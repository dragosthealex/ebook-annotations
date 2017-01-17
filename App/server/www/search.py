import sys
import os
sys.path.insert(0, os.path.abspath('../Generator'))
import json
from smart_ebook_generator.Generator import Generator
from smart_ebook_generator.Utils import BookNotFoundException

if __name__ == '__main__':
  search_type = sys.argv[1]
  query = sys.argv[2]
  generator = Generator()
  if search_type == 'all':
    results = generator.get_json_results(query)
    print(json.dumps(results))
    sys.exit()
  elif search_type == 'single':
    try:
      # The arg query will be an ID
      file_name = generator.generate_html_book(None, query)
      with open(file_name, 'r') as f:
        print(f.read())
    except BookNotFoundException:
      print("Book not found.")
