# -*- coding: utf-8 -*-
"""Test the book searcher."""
import unittest
from ea_generator.book_searcher import BookSearcher
from ea_generator.book import BookSource
from ea_generator.utils import URLS


class TestBookSearcher(unittest.TestCase):
    """Test case for the book searcher."""

    def test_search_for_query(self):
        """Should return the correct results for a given query."""
        pass

    def test_construct_url_from_id(self):
        """Should construct the good URL from the id."""
        searcher = BookSearcher()
        searcher.book_id = '10085'
        url = searcher.construct_url_from_id()
        self.assertIsNot(url, None)
        self.assertEqual(str(url),
                         URLS["MIRRORSERVICE"] +
                         '1/0/0/8/10085/10085-h/10085-h.htm')

    def test_get_book_info(self):
        """Should get the book for the first book that matches the query."""
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
                         URLS["MIRRORSERVICE"] +
                         '1/0/0/8/10085/10085-h/10085-h.htm')
        self.assertEqual(source, BookSource.GUTENBERG)

if __name__ == '__main__':
        unittest.main()
