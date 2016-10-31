# -*- coding: utf-8 -*-

import nltk
import re
from nltk import word_tokenize
from nltk import FreqDist
from nltk.corpus import gutenberg
from nltk.corpus import stopwords
from Annotation import TextAnnotation
from Annotation import AnnotationType

__all__ = ['Analyser']

# TODO: Make annotations user-influenced

class Analyser:
  text = None
  common_words = None
  uncommon_treshold = None

  def __init__(self, text = None):
    self.text = self.process_input(text)
    self.load_common_words()

  # Return the list of Annotation objects with the words and their respective definition
  def generate_annotations(self, text = None):
    if text is None:
      text = self.text
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
    return re.sub('[^a-zA-Z0-9 -]+', ' ', text)

  # Return the nltk Text object from given string
  def nltk_text(self, text):
    text = nltk.Text(word_tokenize(text))

  # Eliminate the common words from a nltk Text list
  def eliminate_common(self, text):
    text = set(w.lower() for w in text if w not in stopwords.words('english'))
    text = set(w for w in text if w not in common_words)
    return text

  # Find out which words / group of words represent a geographical
  # place / historical event / VIP, etc
  # TODO
  def get_extras(self, text):
    return nltk_text('')

  # Load the common words list
  def load_common_words(self):
    with open(COMMON_WORDS_FILE_NAME, 'r') as f:
      self.common_words = nltk_text(f.read())

class Analyser2:

  input_file_name = None
  output_file_name = None
  text = None
  corpus_words = None
  lexical_richness = None
  uncommon_treshold = None

  def __init__(self, input_file, output_file):
    self.input_file_name = input_file
    self.output_file_name = output_file
    self.tokenize_input()
    self.set_corpus()

  def set_corpus(self):
    # TODO : Find way to join all corpora
    """
    words = []
    for fileid in gutenberg.fileids():
      words = words + gutenberg.words(fileid)
    """
    self.corpus_words = gutenberg.words('austen-emma.txt')

  def tokenize_input(self):
    tokens = word_tokenize(self.read_input())
    self.text = nltk.Text(tokens)

  def read_input(self):
    f = open(self.input_file_name, 'r')
    text = f.read()
    text = re.sub('[^a-zA-Z0-9 ]+', '', text)
    text = re.sub('\n', ' ', text)
    return text

  def calculate_commonness_all(self):
    text_with_commonness = []
    text = set(w.lower() for w in self.text if w not in stopwords.words('english'))
    for word in text:
      percentage = self.percentage_comonness(word)
      text_with_commonness.append((word, percentage))
      print word + ' - ' + str(percentage)
    return text_with_commonness

  def percentage_comonness(self, word):
    return 100 * self.corpus_words.count(word.lower()) / float(len(self.corpus_words))

  def get_lexical_richness(self):
    self.lexical_richness = len(set(self.text)) / float(len(self.text))

  def print_txt(self):
    f = open(self.output_file_name, 'w+')
    f.write('lexical richness: ' + str(self.lexical_richness) + '\n\n')
    f.write('word commonness vs gutenberg corpora: ' + '\n' + str(self.calculate_commonness_all()))


if __name__ == '__main__':
  analyser = Analyser('text.txt', 'word_analysis.txt')
  analyser.print_txt()
