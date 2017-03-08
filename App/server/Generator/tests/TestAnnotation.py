# -*- coding: utf-8 -*-
"""Contains the Annotation classes."""
import unittest
import hashlib
import codecs
from context import TextAnnotation
from context import AnnotationType
from context import connect_database


class TestAnnotation(unittest.TestCase):
  """Test case for TextAnnotations."""

  def setUp(self):
    """Called before every test."""
    pass

  def tearDown(self):
    """Called after every test."""
    # Delete from db if it's the case
    m = hashlib.sha256()
    m.update('exquisite')
    conn, c = connect_database()
    c.execute('''DELETE FROM annotations
                 WHERE hash=?''', (m.hexdigest(),))
    conn.commit()
    m = hashlib.sha256()
    m.update('Loch_Ness')
    c.execute('''DELETE FROM annotations
                 WHERE hash=?''', (m.hexdigest(),))
    conn.commit()
    pass

  def test_get_meaning(self):
    """Test if the meaning is retrieved successfully (by API)."""
    ann = TextAnnotation('exquisite', AnnotationType.UNCOMMON_WORD)
    self.assertEqual(ann.data, "Def:&nbsp;extremely beautiful and very" +
                     " delicately made")
    self.assertFalse(ann.get_from_db())

  def test_get_info(self):
    """Test if the info is retrieved successfully (by API)."""
    ann = TextAnnotation('Loch_Ness', AnnotationType.EXTRA)
    with codecs.open('test_annotation.data', 'r', encoding="utf-8") as f:
      self.assertEqual(ann.data, f.read())
    self.assertFalse(ann.get_from_db(case_sensitive=True))

  def test_get_meaning_db(self):
    """Test if the meaning is saved and retrieved successfully from DB."""
    ann = TextAnnotation('exquisite', AnnotationType.UNCOMMON_WORD)
    # Should not be in db now
    self.assertFalse(ann.get_from_db())
    # Put it now
    ann.save_to_db()
    # Should be in db
    self.assertTrue(ann.get_from_db())
    self.assertEqual(ann.data, "Def:&nbsp;extremely beautiful and very" +
                     " delicately made")

  def test_get_info_db(self):
    """Test if the info is saved and retrieved successfully from DB."""
    ann = TextAnnotation('Loch_Ness', AnnotationType.EXTRA)
    # Should not be in db
    self.assertFalse(ann.get_from_db())
    # Put it
    ann.save_to_db(case_sensitive=True)
    # Should be in db
    self.assertTrue(ann.get_from_db(case_sensitive=True))
