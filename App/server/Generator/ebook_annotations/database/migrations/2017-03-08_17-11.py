# -*- coding: utf-8 -*-
"""Migration for annotations table."""
from limigrations.migration import BaseMigration


class Migration(BaseMigration):
  """The migration."""

  def up(self, conn, c):
    """Executed on migrate."""
    c.execute('''CREATE TABLE IF NOT EXISTS annotations
                 (id integer PRIMARY KEY AUTOINCREMENT,
                  hash text UNIQUE,
                  word text,
                  data text,
                  url text,
                  votes integer
                  )''')
    conn.commit()
    c.execute('''CREATE INDEX IF NOT EXISTS annotations_index
                 ON annotations (hash)''')
    conn.commit()

  def down(self, conn, c):
    """Executed on rollback."""
    c.execute('''DROP INDEX IF EXISTS annotations_index''')
    conn.commit()
    c.execute('''DROP TABLE IF EXISTS annotations''')
    conn.commit()
    pass
