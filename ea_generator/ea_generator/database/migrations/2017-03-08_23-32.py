# -*- coding: utf-8 -*-
"""Adding image url to annotations table."""
from limigrations.migration import BaseMigration


class Migration(BaseMigration):
    """The migration."""

    def up(self, conn, c):
        """Executed on migrate."""
        c.execute('''ALTER TABLE annotations
                     ADD image_url TEXT''')
        conn.commit()

    def down(self, conn, c):
        """Executed on rollback."""
        pass
