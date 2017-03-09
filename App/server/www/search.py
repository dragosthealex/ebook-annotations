import sys
import os
sys.path.insert(0, os.path.abspath('../Generator'))
import json
from ebook_annotations.Generator import Generator
from ebook_annotations.Utils import BookNotFoundException
from ebook_annotations.Utils import CachingType

if __name__ == '__main__':
  search_type = sys.argv[1]
  query = sys.argv[2]
  generator = Generator()
  if search_type == 'all':
    results = generator.search_for_query(query)
    print(json.dumps(results))
    sys.exit()
  elif search_type == 'single':
    try:
      # The arg query will be an ID
      file_name = generator.generate_html_book(query, CachingType.NONE, 2)
      with open(file_name, 'r') as f:
        print(f.read())
    except BookNotFoundException:
      print("Book not found.")
