# -*- coding: utf-8 -*-
"""Test the book searcher."""
import unittest
from context import BookSearcher
from context import BookSource


class TestBookSearcher(unittest.TestCase):
  """Test case for the book searcher."""

  def test_search_for_query(self):
    """Test whether the correct json results are retrieved."""
    pass

  def test_construct_url_from_id(self):
    """Test if the correct url is constructed."""
    searcher = BookSearcher()
    searcher.book_id = '10085'
    url = searcher.construct_url_from_id()
    self.assertIsNot(url, None)
    self.assertEqual(str(url),
                     'http://www.mirrorservice.org/sites/gutenberg.org' +
                     '/1/0/0/8/10085/10085-h/10085-h.htm')

  def test_get_book_info(self):
    """Test if the correct book info is retrieved."""
    searcher = BookSearcher()
    searcher.search_query = 'moorish literature'
    # Get the results
    results = searcher.search_for_query()
    # We only care about the first
    first_id = results[0]["id"]
    searcher.book_id = first_id
    # Get the info
    url, the_id, source = searcher.get_book_info()
    # Test the assertions
    self.assertIsNot(the_id, None)
    self.assertIsNot(url, None)
    self.assertIsNot(source, None)
    self.assertEqual(str(the_id), '10085')
    self.assertEqual(str(url),
                     'http://www.mirrorservice.org/sites/gutenberg.org' +
                     '/1/0/0/8/10085/10085-h/10085-h.htm')
    self.assertEqual(source, BookSource.GUTENBERG)

if __name__ == '__main__':
    unittest.main()
