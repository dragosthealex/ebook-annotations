import nltk
import re
from nltk import word_tokenize
from nltk import FreqDist
from nltk.corpus import gutenberg
from nltk.corpus import stopwords

__all__ = ['Analyser']

class Analyser:

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
