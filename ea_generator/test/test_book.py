# -*- coding: utf-8 -*-
"""Tests the Book class."""
import unittest
import os
from ea_generator.book import Book
from ea_generator.book import BookSource
from ea_generator.utils import URLS
from ea_generator.utils import CachingType


class TestBook(unittest.TestCase):
    """Test case for book."""

    def setUp(self):
        """Run before every test."""
        self.book = Book(URLS['MIRRORSERVICE'] + '/1/11/11-h/11-h.htm', '11')

    def tearDown(self):
        """Run after every test."""
        self.book = None

    def test_is_cached_html(self):
        """Should check for cached books."""
        self.assertFalse(self.book.is_cached_html())

    def test_populate_content(self):
        """Should correctly populate the book."""
        self.book.populate_content()
        self.assertIsNot(None, self.book.title)
        self.assertIsNot(None, self.book.author)
        self.assertIsNot(None, self.book.chapter_titles)
        self.assertIsNot(None, self.book.chapters)

    def test_create_annotations(self):
        """Should create the annotations."""
        self.book.populate_content()
        self.book.create_annotations(chapters=2)

    def test_annotate(self):
        """Should create and apply the annotations."""
        self.book.populate_content()
        self.book.create_annotations(chapters=2)
        self.book.annotate(chapters=2)
        self.book.print_text('test.txt')
        self.assertTrue(os.path.isfile('test.txt'))
        os.unlink('test.txt')

    def test_annotate_caching(self):
        """Should create the annotations from cache and apply the."""
        self.book.populate_content()
        self.book.create_annotations(chapters=2,
                                     caching=CachingType.ANNOTATIONS)
        self.book.annotate(chapters=2)

if __name__ == '__main__':
    unittest.main()
