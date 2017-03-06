"""Test the book searcher."""
import unittest
from context import BookSearcher
from context import BookSource


class TestBookSearcher(unittest.TestCase):
  """Test case for the book searcher."""

  def test_get_book_id(self):
    searcher = BookSearcher()
    the_id = searcher.get_book_id('moorish literature')
    self.assertIsNot(the_id, None)
    self.assertEqual(str(the_id), '10085')

  def test_get_html_book_url(self):
    searcher = BookSearcher()
    url = searcher.get_html_book_url('10085')
    self.assertIsNot(url, None)
    self.assertEqual(str(url),
                     'http://www.mirrorservice.org/sites/gutenberg.org' +
                     '/1/0/0/8/10085/10085-h/10085-h.htm')

  def test_search_for(self):
    searcher = BookSearcher()
    url, the_id, source = searcher.search_for('moorish literature')
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
