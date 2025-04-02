import sqlite3
from typing import Optional

from .schema import Schema, Column
from .collection import Collection
from .converter import from_sql_type

class DB:
    """
    A class to represent a database connection and perform operations on it.
    """
    def __init__(self, path: str = "driz.db"):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def close(self):
        """
        Closes the database connection.
        """
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        if exc_type is not None:
            raise exc_val

    def collection(self, name: str, *, schema: Optional[Schema] = None) -> Optional[Collection]:
        """
        Tries to fetch a collection from the database. If it doesn't exist, it creates a new one.

        Args:
            name (str): The name of the table.
            schema (Schema, optional): The schema of the collection. If not provided, it will be fetched from the database.
        """
        if not schema:
            self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{name}'")
            if not self.cursor.fetchone():
                return None
            self.cursor.execute(f"PRAGMA table_info({name})")
            schema = Schema(*[Column(column[1], from_sql_type(column[2])) for column in self.cursor.fetchall()])
        schema.collection = name
        return self._create_collection(schema)

    def _create_collection(self, schema: Schema) -> Collection:
        """
        Creates a table in the database.

        Args:
            schema (Schema): The schema of the table.
        """
        fields = ", ".join(
            f"{field.name} {field.sql_type} {' '.join(field.constraints)}"
            for field in schema.fields
        )
        sql = f"CREATE TABLE IF NOT EXISTS {schema.collection} ({fields})"
        self.cursor.execute(sql)
        self.connection.commit()
        self.cursor.execute(f"PRAGMA table_info({schema.collection})")
        columns = self.cursor.fetchall()
        column_map = {column[1]: column[2] for column in columns}
        for field in schema.fields:
            if field.name not in column_map:
                self.cursor.execute(f"ALTER TABLE {schema.collection} ADD COLUMN {field.name} {field.sql_type}")
                self.connection.commit()
        return Collection(schema.collection, schema, self.connection)