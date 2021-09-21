import time

from django.db import connections
from django.db.utils import OperationalError as dbOperationalError
from psycopg2 import OperationalError as pgOperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """django command to wait for db to be available"""

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except (pgOperationalError, dbOperationalError):
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
