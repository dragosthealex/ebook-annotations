import os
import sys
sys.path.insert(0, os.path.abspath('../Generator'))
from smart_ebook_generator.Generator import Generator
from smart_ebook_generator.Utils import BookNotFoundException

if __name__ == '__main__':
  query = sys.argv[1]
  generator = Generator()
  try:
    file_name = generator.generate_html_book(query)
    with open(file_name, 'r') as f:
      print f.read()
  except BookNotFoundException:
    print "Book not found."

  sys.exit()
