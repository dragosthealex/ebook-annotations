# -*- coding: utf-8 -*-

from Parser import Parser

__all__ = ['Book']

# The parsed book
class Book:

  parser = None;
  title = None
  author = None
  chapter_titles = None
  chapters = None
  output_txt_file_name = None

  def __init__(self, url):

    self.parser = Parser(url)

    self.title = self.parser.get_title()
    self.author = self.parser.get_author()
    self.chapter_titles = self.parser.get_chapter_titles()
    self.chapters = self.parser.get_chapters()

  def set_output_txt(self, file_name):
    self.output_txt_file_name = file_name

  def print_txt(self, file_name = None):
    if file_name is not None:
      fn = file_name
    else:
      fn = self.output_txt_file_name

    f = open(fn, 'w+')
    f.write(self.title + '\n')
    f.write(self.author + '\n\n')
    f.write('Contents' + '\n')
    for chapter_title in self.chapter_titles:
      f.write(chapter_title + '\n')
    f.write('\n\n\n')

    index = 0
    for chapter in self.chapters:
      f.write(self.chapter_titles[index] + '\n\n')
      f.write(chapter + '\n\n\n')
      index = index + 1

    f.close()


if __name__ == '__main__':
  pass
