import unittest
from context import Analyser

class TestAnalyser(unittest.TestCase):

  def test_preprocess_input(self):
    analyser = Analyser()
    test = analyser.preprocess_input('lol. max/keksasdasd>?<".<WOW><12')
    self.assertIsNot(None, test)
    self.assertEqual(test, 'lol  max keksasdasd " WOW 12')

  def test_eliminate_common(self):
    analyser = Analyser("I am very excitability")
    test = analyser.eliminate_common()

    self.assertIsNot(None, test)
    self.assertEqual(len(test), 1)
    self.assertEqual(test.pop(), 'excitability')
