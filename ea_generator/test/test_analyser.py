# coding: utf-8
"""Tests for analyser module."""

import unittest
from ea_generator.analyser import Analyser


class TestAnalyser(unittest.TestCase):
    """Test case for analyser."""

    def test_preprocess_input(self):
        """The process input should remove special chars."""
        analyser = Analyser(None)
        test = analyser.preprocess_input('lol. max/keksasdasd>?<".<WOW><12')
        self.assertIsNot(None, test)
        self.assertEqual(test, "lol max'keksasdasd'WOW'12")

    def test_eliminate_common(self):
        """Common words should be eliminated."""
        analyser = Analyser("it'll be and I am very excitability")
        test = analyser.eliminate_common()

        self.assertIsNot(None, test)
        self.assertEqual(len(test), 1)
        self.assertEqual(test.pop(), 'excitability')

    def test_get_extras(self):
        """Should find out the extra annotations."""
        text = """
        ‘I wonder if I shall fall right through the earth! How funny it’ll
         seem to come out among the people that walk with their heads
         downward! The Antipathies, I think—’ (she was rather glad there
         was no one this time, as it didn’t sound at all the right word)
         ‘—but I shall have to ask them what the name of the country is,
         youknow. Please, Ma’am, is this New Zealand or Australia?’
        """
        analyser = Analyser(text)
        test = analyser.get_extras()
        self.assertEqual(test, ['Antipathies', "Please Ma'am", 'Zealand',
                                'New Zealand', 'Australia'])
