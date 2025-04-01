import sqlite3

from .schema import Schema, Field, AsType
from .table import Table


class DB:
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

    def fetch_table(self, table_name: str) -> Table:
        """
        Gets a table from the database.

        Args:
            table_name (str): The name of the table.
        """
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        if not self.cursor.fetchone():
            raise ValueError(f"Table '{table_name}' does not exist.")
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        columns = self.cursor.fetchall()
        fields = []
        for column in columns:
            fields.append(Field(column[1], AsType.from_sql_type(column[2])))
        schema = Schema(table_name, *fields)
        return Table(table_name, schema, self.connection)

    def create_table(self, schema: Schema) -> Table:
        """
        Creates a table in the database.

        Args:
            schema (Schema): The schema of the table.
        """
        fields = ", ".join(
            f"{field.name} {field.sql_type} {' '.join(field.constraints)}"
            for field in schema.fields
        )
        sql = f"CREATE TABLE IF NOT EXISTS {schema.table_name} ({fields})"
        self.cursor.execute(sql)
        self.connection.commit()
        self.cursor.execute(f"PRAGMA table_info({schema.table_name})")
        columns = self.cursor.fetchall()
        column_map = {column[1]: column[2] for column in columns}
        for field in schema.fields:
            if field.name not in column_map:
                self.cursor.execute(f"ALTER TABLE {schema.table_name} ADD COLUMN {field.name} {field.sql_type}")
                self.connection.commit()
        return Table(schema.table_name, schema, self.connection)