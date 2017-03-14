# -*- coding: utf-8 -*-
"""Book searcher module."""
import requests
from bs4 import BeautifulSoup
from utils import *
from book import BookSource

# TODO : make a cache
# TODO : make cronjob for updating index file

__all__ = ['BookSearcher']


class BookSearcher(object):
    """Deals with searching the books by query / id.

    Attributes:
        search_query (str): The query we are searching for.
        book_id (int): The retrieved book id.
        result_url (str): The url that we got after a search.
    """

    @property
    def search_query(self):  # pragma: no-cover
        """Get the search query."""
        if self._search_query is None:
            raise AttributeError("Attribute search_query was not set.")
        return self._search_query

    @search_query.setter
    def search_query(self, value):  # pragma: no-cover
        """Set the search query."""
        self._search_query = value

    @property
    def book_id(self):  # pragma: no-cover
        """Get the book id."""
        if self._book_id is None:
            raise AttributeError("Attribute book_id was not set.")
        return self._book_id

    @book_id.setter
    def book_id(self, value):  # pragma: no-cover
        """Set the book id."""
        self._book_id = value

    @property
    def result_url(self):  # pragma: no-cover
        """Get the resulted url."""
        if self._result_url is None:
            raise AttributeError("Attribute result_url was not set.")
        return self._result_url

    @result_url.setter
    def result_url(self, value):  # pragma: no-cover
        """Set the resulted url."""
        self._result_url = value

    def __init__(self, search_query=None, book_id=None):
        """Initialise the searcher with an optional query.

        Args:
            search_query (str, optional): The query we will use to search.
        """
        self._search_query = search_query
        self._book_id = book_id
        self._result_url = None

    def search_for_query(self):
        """Get all results for a given query.

        Args:
            query (str, optional): The query used to search. If it is not
                                   provided `self.search_query` will be used.
        Returns:
            A list of dicts containing the book id and title of all the
            resulted books.
        """
        query = self.search_query
        # Search for the item in db
        conn, c = connect_database()
        c.execute('''SELECT * FROM books
                     WHERE title LIKE ?''', ('%' + query.lower() + '%',))
        books = c.fetchall()
        conn.close()
        result = []
        for book in books:
            # Delete book from db if invalid url
            if not self.test_valid_book_url(self
                                            .construct_url_from_id(book[0])):
                self.delete_book_from_db(book[0])
                continue
            result.append({"id": book[0], "title": book[1]})
        return result

    def construct_url_from_id(self, the_id=None):
        """Create the url of the book from its id.

        Args:
            the_id (int, optional): The id of the book. If it is not provided
                                    `self.book_id` will be used.
        Returns:
            The resulted URL.
        """
        if the_id is None:
            the_id = self.book_id
        # The way file resources work is, if we have a book number 12333,
        # then the book is located at 1/2/3/3/12333.htm
        # or 1/2/3/3/12333-h/12333-h.htm
        good_link = ''
        for digit in the_id[:-1]:
            good_link = good_link + digit + '/'
        good_link = good_link + the_id + '/' + the_id +\
            '-h/' + the_id + '-h.htm'

        result_url = URLS['MIRRORSERVICE'] + good_link
        self.result_url = result_url
        return result_url

    def test_valid_book_url(self, url):
        """Test whether a book URL is valid.

        Args:
            url (string, optional): The url to test. If it is not provided
                                    `self.result_url` will be used.
        Returns:
            True if the URL is valid, false otherwise.
        """
        r = requests.get(url)
        self.root = BeautifulSoup(r.content, "html.parser")
        # If no pre, then wrong link
        if len(self.root.find_all('pre')) == 0:
            return False
        if self.root.h2 is None and self.root.h1 is None:
            return False
        return True

    # Do a search from a query
    def get_book_info(self):
        """Get a nicely formated touple containing the resulted book information.

        Args:
            query (str): The query to set the searcher to.
            the_id (int, optional): The id of the book. If it is not provided
                                    `self.book_id` will be used.
        Returns:
            A touple (url, id, source), where url is the book URL, id is the id
            of the book and source is the source where the book was parsed from
            (just Gutenberg for now).
        """
        the_id = self.book_id
        the_url = str(self.construct_url_from_id())
        return (the_url, the_id, BookSource.GUTENBERG)

    def delete_book_from_db(self, the_id):
        """Delete a book from db by ID.

        Args:
            the_id (int): The id of the book that must be deleted.
        """
        # Search the db for id
        conn, c = connect_database()
        c.execute('''DELETE FROM books
                     WHERE id=?''', (the_id,))
        conn.commit()
