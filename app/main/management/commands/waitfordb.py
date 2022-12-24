import time
from psycopg2 import OperationalError as Psycopg20pError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    кастомная команда для ожидания пока встанет бд
    """

    help = "Command for waiting DataBase"

    def handle(self, *args, **options):
        self.stdout.write("waiting for DataBase ...")
        db_up = False
        while not db_up:
            try:
                self.check(databases=['default'])  #?
                db_up = True
            except (Psycopg20pError, OperationalError):
                self.stdout.write("wait, dataBase is starting")
                time.sleep(5)

        self.stdout.write('DAtaBase ready')
