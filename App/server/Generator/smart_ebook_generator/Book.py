# -*- coding: utf-8 -*-

from Parser import GutenbergParser
from Analyser import Analyser

__all__ = ['Book']

# The parsed book
class Book:

  parser = None

  title = None
  author = None
  chapter_titles = None
  chapters = None
  annotations = None

  def __init__(self, url):

    self.parser = GutenbergParser(url)

    self.title = self.parser.get_title()
    self.id = self.parser.get_id()
    self.author = self.parser.get_author()
    self.chapter_titles = self.parser.get_chapter_titles()
    self.chapters = self.parser.get_chapters()

    self.get_annotations()

  # Get the annotations from the chapters
  def get_annotations(self):
    text = ''
    for chapter in self.chapters:
      text += str(chapter)
    analyser = Analyser(text)
    self.annotations = analyser.generate_annotations()

if __name__ == '__main__':
  pass
