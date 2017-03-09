# -*- coding: utf-8 -*-
"""Test for utils module."""
import unittest
import os
from context import *


class TestUtils(unittest.TestCase):
  """Test case for Utils module."""

  def setUp(self):
    """Called before every test."""
    pass

  def tearDown(self):
    """Called after every test."""
    if os.path.isfile(DB_MIGRATIONS_FOLDER + '/test_migration.py'):
      os.unlink(DB_MIGRATIONS_FOLDER + '/test_migration.py')

  def test_connect_db(self):
    """Test whether the connection to db is made."""
    conn, c = None, None
    conn, c = connect_database()
    self.assertIsNot(conn, None)
    self.assertIsNot(c, None)

  def test_enclose_in_tag(self):
    """Test whether the function to enclose in tags works."""
    enclosed_no_attributes = enclose_in_html_tag('title', 'Some title')
    self.assertEqual(enclosed_no_attributes, '<title >Some title</title>')

    enclosed_with_attributes = enclose_in_html_tag('title', 'Some title',
                                                   {'attr': 'awesome'})
    self.assertEqual(enclosed_with_attributes,
                     '<title attr="awesome">Some title</title>')

  def test_recursive_enclose_in_tag(self):
    """Test the tag enclosure function with recursive tags."""
    recursive_enclosed = enclose_in_html_tag('title', 'Some Title')
    recursive_enclosed = enclose_in_html_tag('head', recursive_enclosed)
    self.assertEqual(recursive_enclosed,
                     '<head ><title >Some Title</title></head>')

  def test_migrate(self):
    """Test whether the migration system works."""
    # Create a migration
    with open(DB_MIGRATIONS_FOLDER + "/test_migration.py", "w") as f:
      f.write("""\
from limigrations.migration import BaseMigration

class Migration(BaseMigration):
  def up(self, conn, c):
    c.execute('''CREATE TABLE IF NOT EXISTS test
                 ('col1' text, 'col2' text)''')
    conn.commit()
    c.execute('''INSERT INTO test
                 VALUES (?, ?)''', ('lol', 'stuff'))
    conn.commit()
  def down(self, conn, c):
    pass""")
    # Migrate
    migrate_up()
    # Test whether the table was created
    conn, c = connect_database()
    c.execute("SELECT * FROM test LIMIT 1")
    row = c.fetchone()
    self.assertEqual('lol', row[0])
    self.assertEqual('stuff', row[1])
    # If successful, delete the table
    c.execute("DROP TABLE IF EXISTS test")
    c.execute("""DELETE FROM migrations
                 WHERE file=? """, ('test_migration.py',))
    conn.commit()

  def test_migrate_rollback(self):
    """Test whether the rollback works."""
    # Create a migration
    with open(DB_MIGRATIONS_FOLDER + "/test_migration.py", "w") as f:
      f.write("""\
from limigrations.migration import BaseMigration

class Migration(BaseMigration):
  def up(self, conn, c):
    c.execute('''CREATE TABLE IF NOT EXISTS test
                 ('col1' text, 'col2' text)''')
    conn.commit()
    c.execute('''INSERT INTO test
                 VALUES (?, ?)''', ('lol', 'stuff'))
    conn.commit()
  def down(self, conn, c):
    c.execute('''DROP TABLE IF EXISTS test''')
    conn.commit()""")
    # Migrate and then rollback
    migrate_up()
    migrate_rollback()
    conn, c = connect_database()
    # Test whether rollback works
    c.execute("""SELECT name FROM sqlite_master
                 WHERE type='table' AND name='test'""")
    self.assertEqual(len(c.fetchall()), 0)
    c.execute("DROP TABLE IF EXISTS test")
    c.execute("""DELETE FROM migrations
                 WHERE file=? """, ('test_migration.py',))
    conn.commit()
