import unittest
from context import *

class TestUtils(unittest.TestCase):
  def test_enclose_in_tag(self):
    enclosed_no_attributes = enclose_in_html_tag('title', 'Some title')
    self.assertEqual(enclosed_no_attributes, '<title >Some title</title>')

    enclosed_with_attributes = enclose_in_html_tag('title', 'Some title', {'attr': 'awesome'})
    self.assertEqual(enclosed_with_attributes, '<title attr="awesome">Some title</title>')

  def test_recursive_enclose_in_tag(self):
    recursive_enclosed = enclose_in_html_tag('title', 'Some Title')
    recursive_enclosed = enclose_in_html_tag('head', recursive_enclosed)
    self.assertEqual(recursive_enclosed, '<head ><title >Some Title</title></head>')
