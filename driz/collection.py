import sqlite3
from typing import Optional, Union, Dict, Any, List

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

    def clear(self):
        """
        Clears the contents of the collection.
        """
        self.cursor.execute(f"TRUNCATE TABLE {self.name}")
        self.connection.commit()

    def drop(self, confirm: bool = False):
        """
        Drops the collection from the database.
        """
        if not confirm:
            raise RuntimeWarning("Are you sure you want to drop this table? Use confirm=True to proceed.")
        self.cursor.execute(f"DROP TABLE IF EXISTS {self.name}")
        self.connection.commit()

    def insert(self, **data):
        """
        Insert a row into the table.
        """
        if len(data) != len(self.schema.columns):
            raise ValueError("Data length does not match schema fields length.")
        for field in self.schema.columns:
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

    def fetch(self, key: Union[int, str]) -> Optional[Dict[str, Any]]:
        """
        Fetch all rows from the table.
        """
        self.cursor.execute(f"SELECT * FROM {self.name} WHERE id = ?", (key,))
        data = self.cursor.fetchone()
        if data is None:
            return None
        return dict(zip([column[0] for column in self.cursor.description], data))

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
        return [
            dict(zip([column[0] for column in self.cursor.description], row))
            for row in self.cursor.fetchall()
        ]

    def union(self, other: "Collection") -> List[Dict[str, Any]]:
        """
        Fetch all rows from two collections.
        """
        self.cursor.execute(f"SELECT * FROM {self.name} UNION SELECT * FROM {other.name}")
        return [
            dict(zip([column[0] for column in self.cursor.description], row))
            for row in self.cursor.fetchall()
        ]

    def distinct(self, column: str) -> List[Any]:
        """
        Fetch distinct values from a column.
        """
        self.cursor.execute(f"SELECT DISTINCT {column} FROM {self.name}")
        return [row[0] for row in self.cursor.fetchall()]

    def order_by(self, *columns: str, desc: bool = False) -> List[Dict[str, Any]]:
        """
        Fetch all rows ordered by one or more columns.
        """
        order = "DESC" if desc else "ASC"
        if len(columns) == 0:
            raise ValueError("At least one column must be specified.")
        placeholder = ", ".join(columns)
        self.cursor.execute(f"SELECT * FROM {self.name} ORDER BY {placeholder} {order}")
        return [
            dict(zip([column[0] for column in self.cursor.description], row))
            for row in self.cursor.fetchall()
        ]

    def avg(self, column: str) -> float:
        """
        Calculate the average of a numeric column.
        """
        self.cursor.execute(f"SELECT AVG({column}) FROM {self.name}")
        return self.cursor.fetchone()[0]

    def sum(self, column: str) -> float:
        """
        Calculate the sum of a numeric column.
        """
        self.cursor.execute(f"SELECT SUM({column}) FROM {self.name}")
        return self.cursor.fetchone()[0]

    def min(self, column: str) -> Union[int, float]:
        """
        Calculate the minimum of a numeric column.
        """
        self.cursor.execute(f"SELECT MIN({column}) FROM {self.name}")
        return self.cursor.fetchone()[0]

    def max(self, column: str) -> Union[int, float]:
        """
        Calculate the maximum of a numeric column.
        """
        self.cursor.execute(f"SELECT MAX({column}) FROM {self.name}")
        return self.cursor.fetchone()[0]

    @property
    def count(self) -> int:
        """
        Count the number of rows in the table.
        """
        self.cursor.execute(f"SELECT COUNT(*) FROM {self.name}")
        return self.cursor.fetchone()[0]

    def where(self, *conditions: str):
        """
        Execute a custom SQL query.
        """
        conditions = ", ".join(conditions)
        self.cursor.execute(f"SELECT * FROM {self.name} WHERE {conditions};")
        return [
            dict(zip([column[0] for column in self.cursor.description], row))
            for row in self.cursor.fetchall()
        ]

    def update(self, key: Union[int, str], **data):
        """
        Update a row by its ID.
        """
        allowed = [f.name for f in self.schema.columns]
        for k, v in data.items():
            if k not in allowed:
                raise ValueError(f"Invalid field: {k}")
            if as_sql_type(type(v)) != self.schema.get_column_type(k):
                raise TypeError(f"Incorrect type for field: {k}")
        placeholders = ", ".join(f"{k} = ?" for k in data.keys())
        values = tuple(data.values()) + (key,)
        sql = f"UPDATE {self.name} SET {placeholders} WHERE id = ?"
        self.cursor.execute(sql, values)
        self.connection.commit()
