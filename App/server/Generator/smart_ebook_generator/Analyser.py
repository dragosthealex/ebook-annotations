# -*- coding: utf-8 -*-

import nltk
import re
from nltk import word_tokenize
from nltk import FreqDist
from nltk.corpus import gutenberg
from nltk.corpus import stopwords
from utils import *
from Annotation import TextAnnotation
from Annotation import AnnotationType

__all__ = ['Analyser']

# TODO: Make annotations user-influenced

class Analyser:
  text = None
  common_words = None
  uncommon_treshold = None

  def __init__(self, text = None):
    if text is not None:
      self.text = self.preprocess_input(text)
    self.load_common_words()

  # Return the list of Annotation objects with the words and their respective definition
  def generate_annotations(self, text = None):
    if text is None:
      text = self.text
    else:
      text = self.preprocess_input(text)
    # Make the nltk Text list of words
    text = self.nltk_text(text)

    # Get the uncommon_words
    uncommon_words = self.eliminate_common(text)
    # Get the places / VIPs / hystorical events / etc.
    extras = self.get_extras(text)
    # Generate the annotations
    annotations = []
    for word in uncommon_words:
      annotations.append(TextAnnotation(word, AnnotationType.UNCOMMON_WORD))
    for word in extras:
      annotations.append(TextAnnotation(word, AnnotationType.EXTRA))
    # Return the list of annotations
    return annotations

  # Eliminate punctuation and other tokens except plain words
  def preprocess_input(self, text):
    return re.sub("[^a-zA-Z0-9 -']+", ' ', text)

  # Return the nltk Text object from given string
  def nltk_text(self, text):
    text = nltk.Text(word_tokenize(text))
    return text

  # Eliminate the common words from a nltk Text list
  def eliminate_common(self, text = None):
    if text is None:
      text = self.nltk_text(self.text)
    text = set(w.lower() for w in text if w not in self.common_words)
    text = set(w.lower() for w in text if w not in stopwords.words('english'))
    return text

  # Find out which words / group of words represent a geographical
  # place / historical event / VIP, etc
  # TODO
  def get_extras(self, text):
    return self.nltk_text('')

  # Load the common words list
  def load_common_words(self):
    with open(COMMON_WORDS_FILE_NAME, 'r') as f:
      self.common_words = self.nltk_text(f.read())

if __name__ == '__main__':
  pass
