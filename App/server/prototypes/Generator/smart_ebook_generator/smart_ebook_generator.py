
from get_url_by_title_prototype import *
from parse_ebook_prototype import *
from word_analysis_prototype import *

if __name__ == '__main__':
  title = raw_input('Input the title to search for: \n')
  searcher = UrlSearcher(title, 1)
  searcher.get_public_book_url()
  searcher.get_html_book_url()

  book = Book(searcher.result_url)
  book.print_txt(title + '.txt')

  analyser = Analyser(title + '.txt', title + '_word_analysis.txt')
  analyser.print_txt()
