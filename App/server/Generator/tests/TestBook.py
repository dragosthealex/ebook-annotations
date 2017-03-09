# -*- coding: utf-8 -*-
"""Tests the Book class."""
import unittest
from context import Book
from context import BookSource
from context import URLS
from context import CachingType


class TestBook(unittest.TestCase):
  """Test case for book."""

  def setUp(self):
    """Run before every test."""
    self.book = Book(URLS['MIRRORSERVICE'] + '/1/11/11-h/11-h.htm', '11')

  def tearDown(self):
    """Run after every test."""
    self.book = None

  def test_is_cached_html(self):
    """Test the method that checks for cached books."""
    self.assertTrue(True)

  def test_populate_content(self):
    """Test the book population works."""
    self.book.populate_content()
    self.assertIsNot(None, self.book.title)
    self.assertIsNot(None, self.book.author)
    self.assertIsNot(None, self.book.chapter_titles)
    self.assertIsNot(None, self.book.chapters)

  def test_create_annotations(self):
    """Test that annotations are generated properly."""
    self.book.populate_content()
    self.book.create_annotations(chapters=2)

  def test_annotate(self):
    """Test that annotations are applied."""
    self.book.populate_content()
    self.book.create_annotations(chapters=2)
    self.book.annotate(chapters=2)

  def test_annotate_caching(self):
    """Test that annotations are applied (with caching)."""
    self.book.populate_content()
    self.book.create_annotations(chapters=2, caching=CachingType.ANNOTATIONS)
    self.book.annotate(chapters=2)

if __name__ == '__main__':
  unittest.main()
