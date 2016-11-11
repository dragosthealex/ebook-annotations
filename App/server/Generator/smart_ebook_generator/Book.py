# -*- coding: utf-8 -*-

from Parser import GutenbergParser
from Analyser import Analyser
from Utils import *

__all__ = ['Book', 'BookSource']

# Book source. Currently just gutenberg
class BookSource:
  GUTENBERG = 1

# The parsed book
class Book:

  parser = None

  the_id = None
  title = None
  author = None
  chapter_titles = None
  chapters = None
  annotations = None

  def __init__(self, url, the_id, source = BookSource.GUTENBERG):
    if source == BookSource.GUTENBERG:
      self.parser = GutenbergParser(url)
    self.the_id = the_id

  # Check if we already have the html version of this book
  def is_cached_html(self):
    conn, c = connect_database()
    c.execute('''SELECT html_file_name FROM books WHERE id = ?''', (self.the_id,))
    html_file_name = c.fetchone()[0]
    if html_file_name is None or html_file_name == '':
      return False
    return html_file_name

  # Use the parser to parse everything and get the content
  def populate_content(self):
    self.title = self.parser.get_title()
    self.author = self.parser.get_author()
    self.chapter_titles = self.parser.get_chapter_titles()
    self.chapters = self.parser.get_chapters()
  # Get the annotations from the chapters
  def get_annotations(self):
    text = ''
    for chapter in self.chapters:
      text += str(chapter)
    analyser = Analyser(text)
    self.annotations = analyser.generate_annotations()

if __name__ == '__main__':
  pass
