# -*- coding: utf-8 -*-

import re
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

  # The raw text, including all chapters
  raw_text = None

  def __init__(self, url, the_id, source = BookSource.GUTENBERG):
    if source == BookSource.GUTENBERG:
      self.parser = GutenbergParser(url)
    self.the_id = the_id

  # Check if we already have the html version of this book
  def is_cached_html(self):
    conn, c = connect_database()
    c.execute('''SELECT html_file_name FROM books WHERE id = ?''', \
              (self.the_id,))
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
    self.raw_text = text
    analyser = Analyser(text)
    self.annotations = analyser.generate_annotations()

  # Apply the annotations on the words
  def apply_annotations(self, text = None):
    if text is None:
      text = self.raw_text

    for index, ann in enumerate(self.annotations):
      tag = enclose_in_html_tag('a', str(ann.word), {'class': 'annotation',\
                                                'def': str(ann.data),\
                                                'url': str(ann.url)})
      print tag
      text = re.sub(str(ann.word), tag, text)
    return text

if __name__ == '__main__':
  pass
