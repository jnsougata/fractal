import json
import sqlite3
import warnings
from typing import Any, Dict, Optional


class Page:
    def __init__(self, name: str, conn: sqlite3.Connection):
        self.name = name
        self.conn = conn

    def put(self, **data: Any) -> int:
        """Unconditionally inserts JSON data and returns the inserted row ID."""
        cur = self.conn.execute(
            f"INSERT INTO {self.name} (data) VALUES (?)", (json.dumps(data),)
        )
        self.conn.commit()
        return cur.lastrowid

    def update(self, key: int, **data: Any):
        """Updates a record by its ID, merging with existing JSON data."""
        cur = self.conn.execute(f"SELECT data FROM {self.name} WHERE id = ?", (key,))
        row = cur.fetchone()
        if row:
            existing_data = json.loads(row[0])
            existing_data.update(data)
            self.conn.execute(
                f"UPDATE {self.name} SET data = ? WHERE id = ?",
                (json.dumps(existing_data), key),
            )
            self.conn.commit()
            return key
        else:
            return self.put(**data)

    def get(self, key: int) -> Optional[Dict[str, Any]]:
        """Fetches a record by its ID, parsing JSON data."""
        cur = self.conn.execute(f"SELECT data FROM {self.name} WHERE id = ?", (key,))
        row = cur.fetchone()
        if row:
            return json.loads(row[0])
        else:
            return None

    def query_by_conditions(self, conditions: dict) -> list:
        """
        Query JSON fields in the 'data' column using conditions.
        Supports '=', '>', '<', '>=', '<=', '!=', 'LIKE'.

        Example:
            conditions = {
                "name": "Sougata",
                "age": (">", 20),
                "specs.RAM": ("LIKE", "16%")
            }
        """
        sql_clauses = []
        values = []

        for field_path, condition in conditions.items():
            json_path = "$." + field_path.replace(".", ".")

            if isinstance(condition, tuple):
                operator, val = condition
            else:
                operator, val = "=", condition

            sql_clauses.append(f"json_extract(data, ?) {operator} ?")
            values.extend([json_path, val])

        where_clause = " AND ".join(sql_clauses)
        query = f"SELECT id, data FROM data WHERE {where_clause}"
        cur = self.conn.execute(query, values)

        return [{"id": row[0], "data": json.loads(row[1])} for row in cur.fetchall()]


class KVStore:
    def __init__(self, name: str = ":memory:"):
        """Initializes an schema-less database."""
        self.conn = sqlite3.connect(name)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        if name == ":memory:":
            warnings.warn(
                "Using in-memory database. Data will not persist after program ends."
            )

    def page(self, name: str) -> Page:
        self.conn.execute(
            f"""
                CREATE TABLE IF NOT EXISTS {name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    data TEXT NOT NULL
                )
                """
        )
        self.conn.commit()
        return Page(name, self.conn)

    def close(self):
        """Closes the database connection."""
        self.conn.close()
