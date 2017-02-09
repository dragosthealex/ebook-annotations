#coding: utf-8

import unittest
from context import Analyser


class TestAnalyser(unittest.TestCase):

  def test_preprocess_input(self):
    analyser = Analyser()
    test = analyser.preprocess_input('lol. max/keksasdasd>?<".<WOW><12')
    self.assertIsNot(None, test)
    self.assertEqual(test, "lol max'keksasdasd'WOW'12")

  def test_eliminate_common(self):
    analyser = Analyser("it'll be and I am very excitability")
    test = analyser.eliminate_common()

    self.assertIsNot(None, test)
    self.assertEqual(len(test), 1)
    self.assertEqual(test.pop(), 'excitability')

  def test_get_extras(self):
    text = """
    ‘I wonder if I shall fall right through the earth! How funny it’ll seem to
    come out among the people that walk with their heads downward! The
    Antipathies, I think—’ (she was rather glad there was no one listening,
    this time, as it didn’t sound at all the right word) ‘—but I shall have to
    ask them what the name of the country is, you know. Please, Ma’am, is this
    New Zealand or Australia?’
    """
    analyser = Analyser(text)
    test = analyser.get_extras()
    print(test)
