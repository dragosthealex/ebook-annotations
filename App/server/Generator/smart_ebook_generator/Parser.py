# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup

__all__ = ['Parser']

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
