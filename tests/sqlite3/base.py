from django.db.backends.sqlite3.base import DatabaseWrapper as BaseDatabaseWrapper
from django.db.backends.sqlite3.operations import (
    DatabaseOperations as BaseDatabaseOperations,
)


class DatabaseOperations(BaseDatabaseOperations):
    def integer_field_range(self, internal_type):
        # by default django does not enforce size on SQLite integers
        # because it does not
        # this is required to pass tests without using a real DB
        return self.integer_field_ranges[internal_type]


class DatabaseWrapper(BaseDatabaseWrapper):
    ops_class = DatabaseOperations
