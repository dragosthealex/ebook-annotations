import requests
import json
from Utils import *

__all__ = ['TextAnnotation', 'AnnotationType']

class AnnotationType:
  UNCOMMON_WORD = 0
  EXTRA = 1

class TextAnnotation:

  the_type = None
  word = None
  data = None
  url = None

  def __init__(self, word, the_type):
    self.the_type = the_type
    self.word = word

    if the_type == AnnotationType.UNCOMMON_WORD:
      self.get_meaning()
    elif the_type == AnnotationType.EXTRA:
      self.get_info()

  # Gets the meaning of the set word
  # TODO: Implement code to get the meaning
  def get_meaning(self):
    dict_url = URLS["DICTIONARY_URL"]
    dict_api_url = URLS["DICTIONARY_API_URL"]
    result = json.loads(requests.get(dict_api_url + self.word).content)

    try:
      if result['status'] == 200 and result['total'] > 0:
        self.data = (((result['results'])[0]['senses'])[0]['definition'])[0]
      else:
        self.data = None
    except Exception:
      self.data = None

    self.url = dict_url + self.word

  # Gets the info about the set word (valid for extras)
  # TODO: Implement code to get the info
  def get_info(self):
    self.data = 'Placeholder info here'
    self.url = 'www.example-wikipedia.com'
