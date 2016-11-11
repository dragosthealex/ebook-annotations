import os
from Book import *
from BookSearcher import BookSearcher

__all__ = ['Generator']

class Generator:

  book = None
  html_book_file_name = None
  pdf_book_file_name = None
  searcher = None

  def __init__(self):
    self.searcher = BookSearcher()
    pass

  # Generate the html book given a title.
  # Returns the absolute path to the file
  def generate_html_book(self, query):
    # Get the url and the source from the query
    url, the_id, source = searcher.search_for(query)
    # Create the book from url and source
    book = Book(url, the_id, source)
    # If book cached, return the file
    if(book.is_cached_html()):
      return book.get_html_file_name()
    # Else, parse the book into the object
    book.populate_content()
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
