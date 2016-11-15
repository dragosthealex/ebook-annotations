import unittest
from context import Book
from context import BookSource

class TestBook(unittest.TestCase):

  def test_is_cached_html(self):
    self.assertTrue(True)

  def test_populate_content(self):
    book = Book('http://eremita.di.uminho.pt/gutenberg/1/11/11-h/11-h.htm', '11')
    book.populate_content()

    self.assertIsNot(None, book.title)
    self.assertIsNot(None, book.author)
    self.assertIsNot(None, book.chapter_titles)
    self.assertIsNot(None, book.chapters)

  def test_get_annotations(self):
    book = Book('http://eremita.di.uminho.pt/gutenberg/1/11/11-h/11-h.htm', '11')
    book.populate_content()
    book.get_annotations()

  def test_apply_annotations(self):
    book = Book('http://eremita.di.uminho.pt/gutenberg/1/11/11-h/11-h.htm', '11')
    book.populate_content()
    book.get_annotations()
    book.annotate()

if __name__ == '__main__':
  unittest.main()
