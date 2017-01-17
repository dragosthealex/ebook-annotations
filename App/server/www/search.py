import sys
import os
sys.path.insert(0, os.path.abspath('../Generator'))
import json
from smart_ebook_generator.Generator import Generator

if __name__ == '__main__':
  query = sys.argv[1]
  generator = Generator()
  results = generator.get_json_results(query)
  print(json.dumps(results))
  sys.exit()
