import unittest
from context import Generator

class TestGenerator(unittest.TestCase):

  def test_enclose_in_tag(self):
    generator = Generator()

    enclosed_no_attributes = generator.enclose_in_tag('title', 'Some title')
    self.assertEqual(enclosed_no_attributes, '<title >Some title</title>')

    enclosed_with_attributes = generator.enclose_in_tag('title', 'Some title', {'attr': 'awesome'})
    self.assertEqual(enclosed_with_attributes, "<title attr='awesome'>Some title</title>")

  def test_recursive_enclose_in_tag(self):
    generator = Generator()

    recursive_enclosed = generator.enclose_in_tag('title', 'Some Title')
    recursive_enclosed = generator.enclose_in_tag('head', recursive_enclosed)
    self.assertEqual(recursive_enclosed, '<head ><title >Some Title</title></head>')

if __name__ == '__main__':
    unittest.main()
