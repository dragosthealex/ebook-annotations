# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup

# Test URLs
ALICE = 'http://eremita.di.uminho.pt/gutenberg/1/11/11-h/11-h.htm'
TOM_SAWYER = 'http://eremita.di.uminho.pt/gutenberg/7/74/74-h/74-h.htm'
FAIRY_TALES = 'http://eremita.di.uminho.pt/gutenberg/2/5/9/2591/2591-h/2591-h.htm'
DORIAN = 'http://eremita.di.uminho.pt/gutenberg/1/7/174/174-h/174-h.htm'

__all__ = ['Parser', 'Book']

# Parse the html ebook
class Parser:

  root = None
  # The chapter title can be h2/h3
  chapter_title_tag = None

  def __init__(self, url):
    r = requests.get(url)
    self.root = BeautifulSoup(r.content, "html.parser")
    self.find_chapter_title_tag()

  # Make unicode-converted strings back into utf8, and replace <br> with spaces
  def stringy(self, string):
    def replace_br(string):
      return re.sub('(<br>)|(<br\/>)',' ',string)
    return replace_br(str(string.encode('utf-8').strip()))

  # Get the title of the book
  def get_title(self):
    title = ''
    for child in self.root.h1.descendants:
      title = title + self.stringy(child)
    return title

  # Get the author of the book
  def get_author(self):
    author = ''
    for child in self.root.h2.descendants:
      author = author + self.stringy(child)
    return author

  # Find out whther the chapters are marked by h2 or h3 tags
  def find_chapter_title_tag(self):
    # We assume it's h2. If we don't have too many, it means it's h3
    self.chapter_title_tag = 'h2'
    if len(self.root.find_all(self.filter_chapters)) < 3:
      self.chapter_title_tag = 'h3'

  # Chapters are marked with a h2/h3 tag
  # Filter out the others, such as illustrations and contents table, also marked with h2 tag
  # Also filter out the author
  def filter_chapters(self, tag):
    s = self.stringy(tag.text)
    return s and tag.name == self.chapter_title_tag \
             and not re.compile('(((?i)by *$)|((?i)by ))').search(s) \
             and not re.compile('((?i)^[/\n/\r ]*contents)').search(s) \
             and not re.compile('((?i)^[/\n/\r ]*illustrations)').search(s) \
             and not re.compile('((?i)' + self.get_author() + ')').search(s)

  # Get the table of contents
  def get_chapter_titles(self):
    chapter_titles = []
    chapter_tags = self.root.find_all(self.filter_chapters)
    # Construct the list with chapters
    for chapter_tag in chapter_tags:
      chapter_titles.append(self.stringy(chapter_tag.text))

    return chapter_titles

  def get_chapters(self):
    chapters = []
    chapters.append('')

    for sibling in self.root.find(self.filter_chapters).next_siblings:
      if sibling.name == 'p':
        chapters[-1] = chapters[-1] + self.stringy(sibling.text) + '\n'
      elif sibling.name == self.chapter_title_tag:
        chapters.append('')

    return chapters

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
  book1 = Book(TOM_SAWYER)
  book1.print_txt('sawyer.txt')
  book2 = Book(ALICE)
  book2.print_txt('alice.txt')
  book3 = Book(FAIRY_TALES)
  book3.print_txt('fairy_tales.txt')
  book4 = Book(DORIAN)
  book4.print_txt('dorian.txt')
