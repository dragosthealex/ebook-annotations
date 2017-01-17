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

  # The query that we are searching for
  search_query = None
  # The book id
  book_id = None
  # The URL of the actual HTML book
  result_url = None
  # Whether to display everything

  def __init__(self, search_query=None):
    self.search_query = search_query

  def get_results_for(self, query=None):
    if query is None:
      query = self.search_query
    # Search for the item in db
    conn, c = connect_database()
    c.execute('''SELECT * FROM books
                 WHERE title LIKE ?''', ('%' + query.lower() + '%',))
    books = c.fetchall()
    result = []
    for book in books:
      result.append({"id": book[0], "title": book[1]})
    return result

  # Get the id of the book by searching in db
  def get_book_id(self, query=None):
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

  # Create the url of the book from its id
  def get_html_book_url(self, the_id=None):
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

    result_url = URLS['EREMITA_MIRROR'] + good_link
    self.result_url = result_url
    return result_url

  # Do a search from a query
  def search_for(self, query, the_id=None):
    self.search_query = query
    if the_id is None:
      the_id = self.get_book_id()
    else:
      self.book_id = the_id
    the_url = str(self.get_html_book_url())
    return (the_url, the_id, BookSource.GUTENBERG)


if __name__ == '__main__':
  pass
