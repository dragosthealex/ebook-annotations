import unittest
import random
from context import GutenbergParser
from context import BookSearcher
from context import BookNotFoundException


class TestParser(unittest.TestCase):

  def setUp(self):
    the_id = random.randrange(11, 10000)
    print(the_id)
    b = BookSearcher()
    try:
      self.p = GutenbergParser(b.get_html_book_url(str(the_id)))
    except BookNotFoundException:
      pass

  def test_parse_random_100(self):
    success = 0
    for i in range(100):
      self.setUp()
      t = self.p.get_title()
      a = self.p.get_author()
      ch = self.p.get_chapters()
      if (t != '') and (t is not None) and (a != '') and (a is not None) \
         and (ch is not None) and (len(ch) > 1):
         success += 1
    self.assertTrue(success > 90)
    print(success)

  def test_parse_random_100_old(self):
    success = 0
    for i in range(100):
      self.setUp()
      t = self.p.get_title()
      a = self.p.get_author()
      ch = self.p.get_chapters_2()
      if (t != '') and (t is not None) and (a != '') and (a is not None) \
         and (ch is not None) and (len(ch) > 1):
         success += 1
    self.assertTrue(success > 90)
    print(success)
