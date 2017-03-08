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

  book = None
  html_book_file_name = None
  pdf_book_file_name = None
  searcher = None

  def __init__(self):
    """Initialise the Generator."""
    self.searcher = BookSearcher()
    pass

  def get_json_results(self, query):
    """Searche for a query and returns the possible matches."""
    results = self.searcher.get_results_for(query)
    return results

  def generate_html_book(self, query=None, the_id=None, caching=None):
    """Generate the html book given a title.

    Args:
      query (str): The query to search for. If set, it returns the first
    Returns:
      The absolute path to the generated file.
    """
    # Get the url and the source from the query
    url, the_id, source = self.searcher.search_for(query, the_id)
    # Create the book from url and source
    book = Book(url, the_id, source)
    # If book cached, return the file
    if(book.is_cached_html()):
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


if __name__ == '__main__':

  title = raw_input('Input the title to search for: \n')
  searcher = UrlSearcher2()
  url = searcher.search_for(title)
  print(url)
  book = Book(url)
  book.print_txt(title + '.txt')
