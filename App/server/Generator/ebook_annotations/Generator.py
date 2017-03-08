# -*- coding: utf-8 -*-
"""This module contains the Generator class.

Used to generate the HTML file from a given ID / query.
"""
import os
import sys
import re
import codecs
from Book import *
from BookSearcher import BookSearcher
from Utils import *

__all__ = ['Generator']


class Generator:
  """The main class for of the module.

  Implements the pipeline, providing a method for generating
  a html file for a given ID and returning the results.
  """

  @property
  def book(self):
    """Get the book."""
    if self._book is None:
      raise AttributeError("Attribute book was not set.")
    return self._book

  @book.setter
  def book(self, value):
    """Set the book."""
    self._book = value

  @property
  def html_file_name(self):
    """Get the html book file name."""
    if self._html_file_name is None:
      raise AttributeError("Attribute html_file_name was not set.")
    return self._html_file_name

  @html_file_name.setter
  def html_file_name(self, value):
    """Set the html book file name."""
    self._html_file_name = value

  @property
  def searcher(self):
    """Get the resulted url."""
    if self._searcher is None:
      raise AttributeError("Attribute searcher was not set.")
    return self._searcher

  @searcher.setter
  def searcher(self, value):
    """Set the resulted url."""
    self._searcher = value

  def __init__(self):
    """Initialise the Generator."""
    self._book = None
    self._html_file_name = None
    self._searcher = BookSearcher()

  def search_for_query(self, query):
    """Search for a query and returns the possible matches.

    Params:
      query (str): The query to search for.

    Returns:
      A list of dicts containing the book id and title of all the resulted
      books.
    """
    self.searcher.search_query = query
    results = self.searcher.search_for_query()
    return results

  def generate_html_book(self, the_id, caching=CachingType.NONE):
    """Generate the html book given a title.

    Args:
      query (str): The query to search for. If set, it returns the first
    Returns:
      The absolute path to the generated file.
    """
    # Get the url and the source from the query
    self.searcher.book_id = the_id
    url, the_id, source = self.searcher.get_book_info()
    # Create the book from url and source
    book = Book(url, the_id, source)

    # Check html caching
    if caching in [CachingType.HTML, CachingType.HTML_ANNOTATIONS] and\
       book.is_cached_html():
      return book.get_html_file_name()
    # Else, parse the book into the object
    book.populate_content()
    self.book = book

    # Put title in tags
    title = enclose_in_html_tag('h1', book.title, {'class': 'title'})
    # Put author in tags
    author = enclose_in_html_tag('h2', book.author, {'class': 'author'})
    # Put the table of contents in tags
    table_of_contents = ''
    for index, chapter_title in enumerate(book.chapter_titles):
      chapter_tag = enclose_in_html_tag('a', chapter_title,
                                        {'href': '#ch-' + str(index)})
      table_of_contents += enclose_in_html_tag('li', chapter_tag)
    table_of_contents = enclose_in_html_tag('ul', table_of_contents,
                                            {'class': 'chapter_title'})

    # Annotate the text (in chapters)
    book.get_annotations()
    book.annotate()

    # Put the chapters in tags
    chapters = ''
    for index, chapter in enumerate(book.chapters):
      ch_title = ""
      if len(book.chapter_titles) > 0:
        ch_title = enclose_in_html_tag('a', book.chapter_titles[index],
                                       {'name': 'ch-' + str(index)})
      ch_title = enclose_in_html_tag('h3', ch_title,
                                     {'class': 'chapter-title'})
      # chapter = re.sub(r'(([^\n]*\n[^\n]*)\n)', r'\1<br>', chapter)
      chapter = enclose_in_html_tag('p', chapter, {'class': 'chapter-body'})
      tag = enclose_in_html_tag('div', ch_title + chapter,
                                {'class': 'chapter'})
      chapters += tag
    # Enclose everything in a div tag with class book
    html = enclose_in_html_tag('div', title + author + table_of_contents +
                               chapters, {'class': 'book'})
    file_name = HTML_BOOKS_FOLDER + '/' + str(the_id) + '.html'
    # Create the html file
    with codecs.open(file_name, 'w', encoding="utf-8") as f:
      f.write(html)

    # Return its name
    return file_name


def main():
  """Run this module as stand-alone."""
  title = raw_input('Input the title to search for: \n')
  g = Generator()
  results = g.search_for_query(title)
  if len(results) == 0:
    print("No results.")
    return
  file_name = g.generate_html_book(results[0]["id"])
  print(file_name)
  g.book.print_text(title + '.txt')

if __name__ == '__main__':
  main()
