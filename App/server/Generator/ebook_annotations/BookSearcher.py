"""Book searcher module."""
import requests
import re
from urllib import quote
from bs4 import BeautifulSoup
from Utils import *
from Book import BookSource

# TODO : make a cache
# TODO : make cronjob for updating index file

__all__ = ['BookSearcher']


class BookSearcher:
  """Deals with searching the books by query / id.

  Attributes:
    search_query (str): The query we are searching for.
    book_id (int): The retrieved book id.
    result_url (str): The url that we got after a search.
  """

  search_query = None
  book_id = None
  result_url = None

  def __init__(self, search_query=None):
    """Initialise the searcher with an optional query.

    Args:
      search_query (str, optional): The query we will use to search.
    """
    self.search_query = search_query

  def get_results_for(self, query=None):
    """Get all results for a given query.

    Args:
      query (str, optional): The query used to search. If it is not provided
                             `self.search_query` will be used.
    Returns:
      A list of dicts containing the book id and title of all the resulted
      books.
    """
    if query is None:
      query = self.search_query
    # Search for the item in db
    conn, c = connect_database()
    c.execute('''SELECT * FROM books
                 WHERE title LIKE ?''', ('%' + query.lower() + '%',))
    books = c.fetchall()
    result = []
    for book in books:
      # Delete book from db if invalid url
      if not self.test_valid_book_url(self.get_html_book_url(book[0])):
        self.delete_book_from_db(book[0])
        continue

      result.append({"id": book[0], "title": book[1]})
    return result

  def get_book_id(self, query=None):
    """Get the id of the book by searching in db.

    Args:
      query (str, optional): The query used to search. If it is not provided
                             `self.search_query` will be used.
    Returns:
      The book ID if it is found, else throws BookNotFoundException
    """
    if query is None:
      query = self.search_query
    # Search the db for id
    conn, c = connect_database()
    c.execute('''SELECT id FROM books
                 WHERE title LIKE ?
                 LIMIT 1''', ('%' + query.lower() + '%',))
    book_id = c.fetchone()
    if book_id is None:
      raise BookNotFoundException()
    book_id = book_id[0]
    self.book_id = book_id
    return book_id

  def get_html_book_url(self, the_id=None):
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

  def test_valid_book_url(self, url=None):
    """Test whether a book URL is valid.

    Args:
      url (string, optional): The  url to test. If it is not provided
                             `self.result_url` will be used.
    Returns:
      True if the URL is valid, false otherwise.
    """
    r = requests.get(url)
    self.root = BeautifulSoup(r.content, "html.parser")
    # If no pre, then wrong link
    if len(self.root.find_all('pre')) == 0:
      return False
    return True

  # Do a search from a query
  def search_for(self, query, the_id=None):
    """Search for a given ID, also keeping the query.

    Args:
      query (str): The query to set the searcher to.
      the_id (int, optional): The id of the book. If it is not provided
                             `self.book_id` will be used.
    Returns:
      A touple (url, id, source), where url is the book URL, id is the id
      of the book and source is the source where the book was parsed from
      (just Gutenberg for now).
    """
    self.search_query = query
    if the_id is None:
      the_id = self.get_book_id()
    else:
      self.book_id = the_id
    the_url = str(self.get_html_book_url())
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

if __name__ == '__main__':
  pass
