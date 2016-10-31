import os
from Book import Book
from UrlSearcher import UrlSearcher2

if __name__ == '__main__':

  title = raw_input('Input the title to search for: \n')
  searcher = UrlSearcher2()
  url = searcher.search_for(title)
  print url
  book = Book(url)
  book.print_txt(title + '.txt')
