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

  def __init__(self, url, the_id, source=BookSource.GUTENBERG):
    if source == BookSource.GUTENBERG:
      self.parser = GutenbergParser(url)
    self.the_id = the_id

  # Check if we already have the html version of this book
  def is_cached_html(self):
    conn, c = connect_database()
    c.execute('''SELECT html_file_name FROM books WHERE id = ?''',
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
    # text = ''
    # for chapter in self.chapters:
    #   text += str(chapter)
    # Use analyser for first 2 chapters only
    analyser = Analyser(self.chapters[0] + ' ' + self.chapters[1])
    self.annotations = analyser.generate_annotations()

  def annotate(self):
    for index, chapter in enumerate(self.chapters[:2]):
      self.chapters[index] = self.apply_annotations(chapter)

  # Apply the annotations on the words
  def apply_annotations(self, text):
    # split text into individual words
    words = text.split(' ')
    # Get just the annotation words
    words_to_annotate = [ann.word for ann in self.annotations]
    analyser = Analyser()
    # Deal with multiple words proper nouns
    proposed_ann_word = words[0]
    in_word = False
    number_of_words = 1
    for index, current_word in enumerate(words):
      # We need to remove extra stuff, like when looked for annotations
      current_word = analyser.preprocess_input(current_word)
      # Test next word
      next_word = "~!~"
      if index + 1 < len(words):
        next_word = analyser.preprocess_input(words[index + 1])

      if not in_word:
        if (current_word + " " + next_word) in words_to_annotate:
          proposed_ann_word = current_word + " " + next_word
          number_of_words = 2
          in_word = True
          continue
        else:
          proposed_ann_word = current_word
          number_of_words = 1
      else:
        if (proposed_ann_word + " " + next_word) in words_to_annotate:
          proposed_ann_word += " " + next_word
          number_of_words += 1
          continue
        else:
          in_word = False

      # Check if the word or its lower case version is to be annotated
      if proposed_ann_word in words_to_annotate:
        # Get the annotation tag
        ann = self.annotations[words_to_annotate.index(proposed_ann_word)]
        # We didn't find the meaning
        if ann.data is None:
          continue
        tag = enclose_in_html_tag('a', str(proposed_ann_word),
                                  {'class': 'annotation',
                                   'data-content': '' + ann.data,
                                   'title': "<a href='" + ann.url +
                                   "'>More</a>"})
        # Replace the processed word found with a tag with the annotation
        if number_of_words == 1:
          words[index] = re.sub(proposed_ann_word, tag, current_word)
        else:
          # Delete words
          words[index - number_of_words + 1:index + 1] = []
          # Replace with tag
          words.insert(index - number_of_words + 1, tag)
        # Remove annotation from list
        if ann in self.annotations:
          self.annotations.remove(ann)
          words_to_annotate.remove(proposed_ann_word)
    # Rebuild the original text
    text = ' '.join(words)
    return text


if __name__ == '__main__':
  pass
