import os
from Book import Book
from UrlSearcher import UrlSearcher

__all__ = ['Generator']

class Generator:

  book = None
  html_book_file_name = None
  pdf_book_file_name = None
  url_searcher = None

  def __init__(self):
    url_searcher = UrlSearcher()
    pass

  # Generate the html book given a title.
  # Returns the absolute path to the file
  def generate_html_book(self, query):
    # Get the url from the query
    url = url_searcher.search_for(query)
    # Checked if cached
    if self.get_cached_html_book(url):
      return self.html_book_file_name
    # If not, create a new book from url
    book = Book(url)
    self.book = book
    # Put stuff in tags
    title = self.enclose_in_tag('h1', book.title, {'class': 'title'})
    author = self.enclose_in_tag('h2', book.author, {'class': 'author'})
    table_of_contents = ''
    for index, chapter_title in enumerate(book.chapter_titles):
      chapter_tag = self.enclose_in_tag('a', chapter_title, {'href': '#ch-' + index})
      ch_titles += self.enclose_in_tag('li', chapter_tag)
    table_of_contents = self.enclose_in_tag('ul', table_of_contents, {'class', 'chapter_title'})
      
  # Enclose some data in a given tag
  def enclose_in_tag(self, tag, data, attributes = {}):
    text = '<' + str(tag) + ' ' + \
      ' '.join(str(key)+"='"+str(value)+"'" for key,value in attributes.iteritems()) + \
      '>'
    text += str(data)
    text += '</' + tag + '>'
    return text

if __name__ == '__main__':

  title = raw_input('Input the title to search for: \n')
  searcher = UrlSearcher2()
  url = searcher.search_for(title)
  print url
  book = Book(url)
  book.print_txt(title + '.txt')
