
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
    self.data = 'Placeholder meaning here'
    self.url = 'www.example-dictionary.com'

  # Gets the info about the set word (valid for extras)
  # TODO: Implement code to get the info
  def get_info(self):
    self.data = 'Placeholder info here'
    self.url = 'www.example-wikipedia.com'
