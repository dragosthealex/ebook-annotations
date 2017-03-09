# -*- coding: utf-8 -*-
"""Module contains the Analyser class."""

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
  """Analyses the text and provides methods for annotating.

  Attributes:
    text (str): The text that is currently analysed.
    common_words (str): A string of English common words
    uncommon_treshold (int): How many votes should the annotation
                             have to be considered uncommon?
  """

  @property
  def uncommon_treshold(self):
    """Get the uncommon_treshold."""
    if self._uncommon_treshold is None:
      raise AttributeError("Attribute uncommon_treshold was not set.")
    return self._uncommon_treshold

  @uncommon_treshold.setter
  def uncommon_treshold(self, value):
    """Set the uncommon_treshold."""
    if value > 100:
      value = 100
    elif value < -100:
      value = -100
    self._uncommon_treshold = value

  def __init__(self, text):
    """Initialise the Analyser."""
    if text is not None:
      self.text = self.preprocess_input(text)
    else:
      self.text = None
    self.common_words = None
    self._uncommon_treshold = -100
    self.load_common_words()

  # Return the list of Annotation objects with the words and their respective
  # definition
  def generate_annotations(self, caching=CachingType.NONE):
    """Generate the annotations for the current text.

    Args:
      caching (:obj:CachingType, optional, default=0): What caching type to
                                      use. Can be CachingType.NONE,
                                      CachingType.ANNOTATIONS,
                                      CachingType.HTML,
                                      CachingType.HTML_ANNOTATIONS
    """
    # Make the nltk Text list of words
    text = self.nltk_text(self.text)

    # Get the uncommon_words
    uncommon_words = self.eliminate_common(text)
    # Get the places / VIPs / hystorical events / etc.
    extras = self.get_extras(text)
    # Generate the annotations
    annotations = []
    for word in uncommon_words:
      annotations.append(TextAnnotation(word, AnnotationType.UNCOMMON_WORD,
                                        caching))
    for word in extras:
      annotations.append(TextAnnotation(word, AnnotationType.EXTRA, caching))
    # Return the list of annotations
    return annotations

  def preprocess_input(self, text):
    """Eliminate punctuation and other tokens except plain words."""
    text = re.sub(ur"([^a-zA-Z0-9 -]+ +[^a-zA-Z0-9 -]*|[^a-zA-Z0-9 -]* +[^a-zA-Z0-9 -]+)", ' ', text)
    text = re.sub(ur"([^a-zA-Z0-9 -]+$|^[^a-zA-Z0-9 -]+)", '', text)
    text = re.sub(ur"([a-zA-Z0-9 -]+?)([^a-zA-Z0-9 -])([a-zA-Z0-9 -]+?)",
                  r"\1'\3", text)
    text = re.sub(ur"([\x00-\x7F -]+?)([^a-zA-Z0-9 -]+)([\x00-\x7F -]+?)",
                  ur"\1'\3", text).encode("utf-8")
    return re.sub(ur"([^a-zA-Z0-9 \-\'])", '', text)

  def nltk_text(self, text):
    """Convert the text to nltk.Text.

    Returns:
      The converted text (nltk.Text instance)
    """
    text = nltk.Text(word_tokenize(text))
    return text

  def eliminate_common(self, text=None):
    """Eliminate the common words from a nltk Text list.

    Args:
      text (:obj:nltk.Text): The text to eliminate common words
                             from.

    Returns:
      The original text without the common words.
    """
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

  def get_extras(self, text=None):
    """Filter the proper nouns.

    Filters the words that are most likely proper nouns, in
    order to process them as annotations of type EXTRA.

    Returns:
      A list of the words that are most likely proper nouns.
    """
    if text is None:
      text = self.nltk_text(self.text)
    # Tag parts of speech
    tagged = nltk.pos_tag(text)
    # Try for composed NNP / NNPS
    isProperNoun = False
    text = []
    properNoun = ""
    for index, (word, tag) in enumerate(tagged):
      if not isProperNoun and (tag == 'NNP' or tag == 'NNPS'):
        # Start building a proper noun
        properNoun = word
        # Set it true
        isProperNoun = True
        # Add it to annotations anyway
        text.append(word)
      elif tag == 'NNP' or tag == 'NNPS':
        # Previous was proper noun. So it may be combined
        properNoun += " " + word
        # Add the single word to annotations anyway, in case it might be not
        text.append(word)
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
    # Eliminate common
    result = [w for w in result if w.lower() not in self.common_words and
              w.lower() not in stopwords.words('english')]
    return result

  def load_common_words(self):
    """Load the common words list."""
    with open(COMMON_WORDS_FILE_NAME, 'r') as f:
      self.common_words = self.nltk_text(f.read().decode('utf-8'))


if __name__ == '__main__':
  pass
