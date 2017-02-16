# -*- coding: utf-8 -*-

import nltk
import re
from nltk import word_tokenize
from nltk import FreqDist
from nltk.corpus import gutenberg
from nltk.corpus import stopwords
from Utils import *
from Annotation import TextAnnotation
from Annotation import AnnotationType

__all__ = ['Analyser']

# TODO: Make annotations user-influenced


class Analyser:
  text = None
  common_words = None
  uncommon_treshold = None

  def __init__(self, text=None):
    if text is not None:
      self.text = self.preprocess_input(text)
    self.load_common_words()

  # Return the list of Annotation objects with the words and their respective
  # definition
  def generate_annotations(self, text=None):
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
    text = re.sub(ur"([^a-zA-Z0-9 -]+ +[^a-zA-Z0-9 -]*|[^a-zA-Z0-9 -]* +[^a-zA-Z0-9 -]+)", ' ', text)
    text = re.sub(ur"([^a-zA-Z0-9 -]+$|^[^a-zA-Z0-9 -]+)", '', text)
    text = re.sub(ur"([a-zA-Z0-9 -]+?)([^a-zA-Z0-9 -])([a-zA-Z0-9 -]+?)",
                  r"\1'\3", text)
    text = re.sub(ur"([\x00-\x7F -]+?)([^a-zA-Z0-9 -]+)([\x00-\x7F -]+?)",
                  ur"\1'\3", text).encode("utf-8")
    return re.sub(ur"([^a-zA-Z0-9 \-\'])", '', text)

  # Return the nltk Text object from given string
  def nltk_text(self, text):
    text = nltk.Text(word_tokenize(text))
    return text

  # Eliminate the common words from a nltk Text list
  def eliminate_common(self, text=None):
    if text is None:
      text = self.nltk_text(self.text)
    # Remove the upper case words
    # Remove common words
    # Remove stopwords
    # TODO: maybe check just for nouns / verbs ???
    text = set(w for w in text if w == w.lower() and
               w.lower() not in self.common_words and
               w.lower() not in stopwords.words('english'))

    return text

  # Find out which words / group of words represent a geographical
  # place / historical event / VIP, etc
  # TODO
  def get_extras(self, text=None):
    return self.nltk_text("")
    if text is None:
      text = self.nltk_text(self.text)
    # Tag parts of speech
    tagged = nltk.pos_tag(text)
    # Try for composed NNP / NNPS
    isProperNoun = False
    text = []
    properNoun = ""
    print(tagged)
    for index, (word, tag) in enumerate(tagged):
      if not isProperNoun and (tag == 'NNP' or tag == 'NNPS'):
        # Start building a proper noun
        properNoun = word
        # Set it true
        isProperNoun = True
        # Add it to annotations anyway
        text.append(word)
        print(word + " -> nnp")
      elif tag == 'NNP' or tag == 'NNPS':
        # Previous was proper noun. So it may be combined
        properNoun += " " + word
        # Add the single word to annotations anyway, in case it might be not
        text.append(word)
        print(word + " -> nnp2")
      elif isProperNoun and tag == 'IN':
        # Add what we have by now to the text
        text.append(properNoun)
        # Previous was proper noun. So it may be composed
        properNoun += " " + word
      elif isProperNoun:
        # Add what we have by now to the text
        text.append(properNoun)
        # Finished with proper noun, so set it false
        isProperNoun = False

    # Remove duplicates
    seen = {}
    result = []
    for w in text:
      if w in seen:
        continue
      seen[w] = 1
      result.append(w)

    return result

  # Load the common words list
  def load_common_words(self):
    with open(COMMON_WORDS_FILE_NAME, 'r') as f:
      self.common_words = self.nltk_text(f.read().decode('utf-8'))


if __name__ == '__main__':
  pass
