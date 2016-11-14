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
    analyser = Analyser(text)
    self.annotations = analyser.generate_annotations()

  def annotate(self):
    for chapter in self.chapters:
      self.apply_annotations(chapter)

  # Apply the annotations on the words
  def apply_annotations(self, text):
    # split text into individual words
    words = text.split(' ')
    # Get just the annotation words
    words_to_annotate = [ann.word for ann in self.annotations]
    analyser = Analyser()
    for index, current_word in enumerate(words):
      # We need to remove extra stuff, like when looked for annotations
      processed_word = sorted(analyser.preprocess_input(current_word).split())[-1]
      if processed_word in words_to_annotate:
        # Get the annotation tag
        ann = self.annotations[words_to_annotate.index(processed_word)]
        tag = enclose_in_html_tag('a', str(processed_word), {'class': 'annotation',\
                                                  'def': str(ann.data),\
                                                  'url': str(ann.url)})
        # Replace the processed word found with a tag with the annotation
        words[index] = re.sub(processed_word, tag, current_word)
    # Rebuild the original text
    text = ' '.join(words)
    return text

if __name__ == '__main__':
  pass
