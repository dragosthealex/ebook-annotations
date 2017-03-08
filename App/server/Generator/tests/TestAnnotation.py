# -*- coding: utf-8 -*-
"""Contains the Annotation classes."""
import unittest
from context import TextAnnotation
from context import AnnotationType


class TestAnnotation(unittest.TestCase):
  """Test case for TextAnnotations."""

  def setUp(self):
    """Called before every test."""
    pass

  def tearDown(self):
    """Called after every test."""
    pass

  def test_get_meaning(self):
    """Test if the meaning is retrieved successfully (by API)."""
    ann = TextAnnotation('exquisite', AnnotationType.UNCOMMON_WORD)
    self.assertEqual(ann.data, "Def:&nbsp;extremely beautiful and very" +
                     " delicately made")
    self.assertFalse(ann.get_from_db())

  def test_get_info(self):
    """Test if the info is retrieved successfully (by API)."""
    ann = TextAnnotation('Lochness', AnnotationType.UNCOMMON_WORD)
    self.assertEqual(ann.data, "Def:&nbsp;extremely beautiful and very" +
                     " delicately made")
    self.assertFalse(ann.get_from_db())
    pass

  def test_get_meaning_db(self):
    """Test if the meaning is retrieved successfully (by DB)."""
    pass

  def test_get_info_db(self):
    """Test if the info is retrieved successfully (by DB)."""
    pass
