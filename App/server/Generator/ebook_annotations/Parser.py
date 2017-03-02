# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
from Utils import BookNotFoundException

__all__ = ['GutenbergParser']


# Parser class
class Parser():

  def stringy(self, string):
    """
    Make unicode-converted strings back into utf8, and replace <br> with spaces.
    """
    if not string or string is None or string == '':
      return ''

    try:
      def replace_br(string):
        return re.sub(r'(<br>)|(<br\/>)', ' ', string)
      return replace_br(string.strip()) + ' '
    except TypeError:
      return ''

  def get_title(self):
    pass

  def get_author(self):
    pass

  def get_chapter_titles(self):
    pass

  def get_chapters(self):
    pass


# Parse the html ebook from gutenberg
class GutenbergParser(Parser):

  # The url of the html book
  url = None
  # The root element
  root = None
  # The chapter title can be h2/h3
  chapter_title_tag = None

  def __init__(self, url):
    r = requests.get(url)
    # Extract all line breaks
    content = re.sub(r'(?i)(\<br\>|\<\/br\>|\< \/br\>|\<\/ br\>|\< \\br\>)', '', r.content)
    self.root = BeautifulSoup(content, "html.parser")
    # If no pre, then wrong link
    if len(self.root.find_all('pre')) == 0:
      raise BookNotFoundException('Invalid book ID')
    # Extract last pre
    self.root.find_all('pre')[-1].extract()
    self.find_chapter_title_tag()
    self.url = url

  def get_title(self):
    """
    Returns the title of the book, from the H1 element.
    """
    title = ''
    if self.root.h1 is None:
      for child in self.root.h2.descendants:
        title = title + self.stringy(child)
      return title
    # else
    for child in self.root.h1.descendants:
      title = title + self.stringy(child)
    return title

  def get_author(self):
    """
    Returns the author of the book, using either H1 or H2 elements.
    """
    author = ''
    # Try with h1
    if self.root.h2 is None:
      for child in self.root.h1.descendants:
        author = author + self.stringy(child)
      return author
    # Else
    for child in self.root.h2.descendants:
      author = author + self.stringy(child)
    return author

  def find_chapter_title_tag(self):
    """
    Find what tag corresponds to chapter titles. Can be either H2 or H3.
    Set the attribute with the tag name.
    """
    # We assume it's h2. If we don't have too many, it means it's h3
    self.chapter_title_tag = 'h2'
    if len(self.root.find_all(self.filter_chapters)) < 3:
      self.chapter_title_tag = 'h3'

  def filter_chapters(self, tag):
    """
    Function that takes a tag and returns true if it's probable to be a
    title of a chapter.
    """
    s = self.stringy(tag.text)
    return s and tag.name == self.chapter_title_tag \
        and not re.compile('((?i)Part)').search(s) \
        and not re.compile('(((?i)by *$)|((?i)by ))').search(s) \
        and not re.compile('((?i)^[/\n/\r ]*contents)').search(s) \
        and not re.compile('((?i)^[/\n/\r ]*illustrations)').search(s) \
        and not re.compile('((?i)' + self.get_author() + ')').search(s)

  def get_chapter_titles(self):
    """
    Get a list with the chapter titles.
    """
    chapter_titles = []
    chapter_tags = self.root.find_all(self.filter_chapters)
    # Construct the list with chapters
    for chapter_tag in chapter_tags:
      chapter_titles.append(self.stringy(chapter_tag.text))

    return chapter_titles

  def get_chapters_2(self):
    """
    Old function for getting chapters.
    """
    chapters = []
    chapters.append('')
    for sibling in self.root.find(self.filter_chapters).next_siblings:
      if sibling.name == 'p':
        chapters[-1] = chapters[-1] + self.stringy(sibling.text) + '\n'
      elif sibling.name == self.chapter_title_tag:
        chapters.append('')
    return chapters

  def get_chapters(self):
    """
    Get a list of chapters in the book. Based on the chapter titles tags,
    which can be H2 or H3. Returns just the text of the chapters.
    """
    # Initialise chapters
    chapters = []
    chapters.append('')
    i = 0
    # If no chapter seen, it means no chapters, so assume there aren't any
    if self.root.find(self.filter_chapters) is None:
      for node in self.root.h1.find_all_next():
        chapters[i] += node.text
      return chapters
    # Iterate over all text except chapter nodes
    for node in self.root.find(self.filter_chapters).find_all_next():
      # If we find another chapter tag, we continue
      if self.filter_chapters(node):
        i += 1
        chapters.append('')
      else:
        # Else we append the text to current chapter
        chapters[i] += node.text
    return chapters
