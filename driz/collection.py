import sqlite3
from typing import Union, Optional

from .schema import Schema, as_sql_type


class Collection:
    """
    A class to represent a table with headers and rows.
    """

    def __init__(
        self,
        name: str,
        schema: Schema,
        connection: sqlite3.Connection,
    ):
        """
        Initialize the table with headers.
        """
        self.name = name
        self.schema = schema
        self.connection = connection
        self.cursor = connection.cursor()

    def insert(self, **data):
        """
        Insert a row into the table.
        """
        if len(data) != len(self.schema.fields):
            raise ValueError("Data length does not match schema fields length.")
        for field in self.schema.fields:
            if field.name not in data:
                raise ValueError(f"Missing field: {field.name}")
            if str(as_sql_type(type(data[field.name]))) != field.sql_type:
                raise TypeError(f"Incorrect type for field: {field.name}")

        columns = ", ".join(data.keys())
        placeholders = ", ".join("?" * len(data))
        values = tuple(data.values())
        sql = f"INSERT INTO {self.name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(sql, values)
        self.connection.commit()
        return self.cursor.lastrowid

    def delete(self, key: int):
        """
        Delete a row by its ID.
        """
        self.cursor.execute(f"DELETE FROM {self.name} WHERE id = ?", (key,))
        self.connection.commit()

    def fetch(self, key: Union[int, str]) -> Optional[dict]:
        """
        Fetch all rows from the table.
        """
        if isinstance(key, int):
            self.cursor.execute(f"SELECT * FROM {self.name} WHERE id = ?", (key,))
        elif isinstance(key, str):
            self.cursor.execute(f"SELECT * FROM {self.name} WHERE name = ?", (key,))
        else:
            raise TypeError("Key must be either an integer or a string.")
        return self.cursor.fetchone()

    def __iter__(self):
        """
        Iterate over the rows in the table.
        """
        self.cursor.execute(f"SELECT * FROM {self.name}")
        for row in self.cursor.fetchall():
            yield dict(zip([column[0] for column in self.cursor.description], row))

    def all(self):
        """
        Fetch all rows from the table.
        """
        self.cursor.execute(f"SELECT * FROM {self.name}")
        return [dict(zip([column[0] for column in self.cursor.description], row)) for row in self.cursor.fetchall()]