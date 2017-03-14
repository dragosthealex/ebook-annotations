# -*- coding: utf-8 -*-
"""Test for the parser module."""
import unittest
import random
from ea_generator.parser import GutenbergParser
from ea_generator.book_searcher import BookSearcher
from ea_generator.utils import BookNotFoundException


class TestParser(unittest.TestCase):
    """Test case for parser."""

    def setUp(self):
        """Run before every test."""
        b = BookSearcher()
        good_book = False
        while not good_book:
            try:
                the_id = random.randrange(11, 10000)
                self.p = GutenbergParser(b.construct_url_from_id(str(the_id)))
                good_book = True
            except Exception:
                good_book = False

    def test_parse_random_100(self):
        """Should have more than 90 successful parses."""
        success = 0
        for i in range(100):
            self.setUp()
            t = self.p.get_title()
            a = self.p.get_author()
            ch = self.p.get_chapters()
            if (t != '') and (t is not None) and (a != '') \
                    and (a is not None) and (ch is not None) and (len(ch) > 1):
                 success += 1
        self.assertTrue(success > 90)
        print(success)

    def test_parse_random_100_old(self):
        """Should be worse than new parser."""
        success = 0
        for i in range(100):
            self.setUp()
            try:
                t = self.p.get_title()
                a = self.p.get_author()
                ch = self.p.get_chapters_2()
                if (t != '') and (t is not None) and (a != '') \
                        and (a is not None) and (ch is not None) \
                        and (len(ch) > 1):
                    success += 1
            except Exception:
                self.assertTrue(success < 90)
                return
        self.assertTrue(success < 90)
        print(success)
