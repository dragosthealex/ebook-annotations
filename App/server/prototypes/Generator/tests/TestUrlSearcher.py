import unittest
from context import UrlSearcher2

class TestUrlSearcher(unittest.TestCase):

  def test_get_book_id(self):
    searcher = UrlSearcher2()
    the_id = searcher.get_book_id('moorish literature')
    self.assertIsNot(the_id, None)
    self.assertEqual(str(the_id), '10085')

  def test_get_html_book_url(self):
    searcher = UrlSearcher2()
    url = searcher.get_html_book_url('10085')
    self.assertIsNot(url, None)
    self.assertEqual(str(url), \
      'http://eremita.di.uminho.pt/gutenberg/1/0/0/8/10085/10085-h/10085-h.htm')

  def test_search_for(self):
    searcher = UrlSearcher2()
    searcher.search_for('moorish literature')
    self.assertIsNot(searcher.book_id, None)
    self.assertIsNot(searcher.result_url, None)
    self.assertEqual(str(searcher.book_id), '10085')
    self.assertEqual(str(searcher.result_url), \
      'http://eremita.di.uminho.pt/gutenberg/1/0/0/8/10085/10085-h/10085-h.htm')

if __name__ == '__main__':
    unittest.main()
