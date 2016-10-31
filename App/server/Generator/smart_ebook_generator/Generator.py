import os
from Book import Book
from UrlSearcher import UrlSearcher2

class Generator:

  book = None

  def __init__(self):
    pass

  # Generate the html book given a title.
  # Returns the absolute path to the file
  def generate_html(self, title):
    pass

if __name__ == '__main__':

  title = raw_input('Input the title to search for: \n')
  searcher = UrlSearcher2()
  url = searcher.search_for(title)
  print url
  book = Book(url)
  book.print_txt(title + '.txt')
