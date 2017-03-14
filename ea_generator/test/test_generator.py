# -*- coding: utf-8 -*-
"""Test for the generator module."""
import unittest
import os
from ea_generator.generator import Generator
from ea_generator.utils import CachingType
from ea_generator.utils import HTML_BOOKS_FOLDER


class TestGenerator(unittest.TestCase):
    """Test case for generator."""

    def setUp(self):
        """Run before every test."""
        self.g = Generator()

    def test_search_for_query(self):
        """Should search for given query."""
        results = self.g.search_for_query('moorish literature')
        first_id = results[0]["id"]
        self.assertEqual(str(first_id), '10085')

    def test_generate_html_book_no_caching(self):
        """Should generate the html book."""
        file = self.g.generate_html_book('11', CachingType.ANNOTATIONS, 2)
        self.assertIsNot(file, None)
        self.assertEqual(file, 'ea_generator\../html-books/11.html')
        self.assertTrue(os.path.isfile(HTML_BOOKS_FOLDER + '/11.html'))

if __name__ == '__main__':
    unittest.main()
