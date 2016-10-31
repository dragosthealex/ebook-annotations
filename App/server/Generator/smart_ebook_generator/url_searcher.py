import requests
import re
from urllib import quote
from bs4 import BeautifulSoup
from Utils import *

# TODO : make a cache
# TODO : make cronjob for updating index file

__all__ = ['UrlSearcher2']

class UrlSearcher2:

  # The query that we are searching for
  search_query = None
  # The book id
  book_id = None
  # The URL of the actual HTML book
  result_url = None
  # Whether to display everything

  def __init__(self, search_query = None):
    self.search_query = search_query

  # Get the id of the book by searching in db
  def get_book_id(self, query = None):
    if query is None:
      query = self.search_query
    # Search the db for id
    conn, c = connect_database()
    c.execute('''SELECT id FROM books
                 WHERE title LIKE ?''', ('%'+query.lower()+'%',))
    book_id = c.fetchone()[0]
    self.book_id = book_id
    return book_id

  # Create the url of the book from its id
  def get_html_book_url(self, the_id = None):
    if the_id is None:
      the_id = self.book_id
    # The way file resources work is, if we have a book number 12333,
    # then the book is located at 1/2/3/3/12333.htm
    # or 1/2/3/3/12333-h/12333-h.htm
    good_link = ''
    for digit in the_id[:-1]:
      good_link = good_link + digit + '/'
    good_link = good_link + the_id + '/' + the_id \
                + '-h/' + the_id + '-h.htm'

    result_url = URLS['EREMITA_MIRROR'] + good_link
    self.result_url = result_url
    return result_url
  # Do a search from a query
  def search_for(self, query):
    self.search_query = query
    self.get_book_id()
    return str(self.get_html_book_url())

class UrlSearcher:

  # The query that we are searching for
  search_query = None
  # The url on which we append the query
  search_url = None
  # Public URL of the book (where it can be downloaded, etc)
  book_url = None
  # The URL of the actual HTML book
  result_url = None
  # Whether to display everything
  verbose = 0

  def __init__(self, search_query, verbose = 0):
    self.search_query = search_query
    self.search_url = URLS['GUTENBERG_SEARCH']
    self.verbose = verbose

  def get_public_book_url(self):
    r = requests.get(self.search_url + quote(self.search_query))

    f = open('title_search_results.txt', 'a')

    # Output crude result
    if self.verbose is 2:
      f.write(r.content + '\n')

    # Get the list of results
    results = BeautifulSoup(r.content, 'html.parser').find_all('li', class_='booklink')
    # We assume the first is the correct one
    self.book_url = 'http://www.gutenberg.org' + results[0].a['href']

    if self.verbose is not 0:
      f.write('book url: ' + self.book_url + '\n')

    f.close()

  def get_html_book_url(self):
    r = requests.get(self.book_url)

    f = open('title_search_results.txt', 'a')

    if self.verbose is 2:
      f.write(r.content + '\n')

    result = BeautifulSoup(r.content, 'html.parser').find_all('div', id='download')[0]
    result = re.sub('(.*www\.gutenberg\.org\/files\/)', '', result.find_all('tr')[1].find_all('td')[1].a['href'])
    book_number = result.split('/')[0]

    # The way file resources work is, if we have a book number 12333, then the book is located at
    # 1/2/3/3/12333.htm or 1/2/3/3/12333-h/12333-h.htm
    good_link = ''
    for digit in book_number[:-1]:
      good_link = good_link + digit + '/'
    good_link = good_link + result

    self.result_url = URLS['EREMITA_MIRROR'] + good_link

    if self.verbose is not 0:
      f.write('result url: ' + self.result_url + '\n')


if __name__ == '__main__':
  pass
