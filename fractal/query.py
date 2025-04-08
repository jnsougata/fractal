"""
fractal.query
~~~~~~~~~~~~~~~~~~~~~

A module containing functions for building SQL-like query conditions.

:copyright: (c) 2025-present Sougata Jana
:license: MIT, see LICENSE for more details.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    from .collection import Collection

__all__ = ["_Select", "cond", "Condition"]


class Condition:
    def __init__(self, field: str, clause: str = None, values: Optional[Any] = None):
        self.field = field
        self.clause = clause
        self.values = values

    def __eq__(self, other):
        if other is None:
            self.clause = f"{self.field} IS NULL"
            self.values = []
        else:
            self.clause = f"{self.field} = ?"
            self.values = [other]
        return Condition(self.field, self.clause, self.values)

    def __ne__(self, other):

        if other is None:
            self.clause = f"{self.field} IS NOT NULL"
            return self.clause, []
        else:
            self.clause = f"{self.field} != ?"
            self.values = [other]
            return Condition(self.field, self.clause, self.values)

    def __lt__(self, other):
        self.clause = f"{self.field} < ?"
        self.values = [other]
        return Condition(self.field, self.clause, self.values)

    def __le__(self, other):
        self.clause = f"{self.field} <= ?"
        self.values = [other]
        return Condition(self.field, self.clause, self.values)

    def __gt__(self, other):
        self.clause = f"{self.field} > ?"
        self.values = [other]
        return Condition(self.field, self.clause, self.values)

    def __ge__(self, other):
        self.clause = f"{self.field} >= ?"
        self.values = [other]
        return Condition(self.field, self.clause, self.values)

    def startswith(self, other):
        self.clause = f"{self.field} LIKE ?"
        self.values = [f"{other}%"]
        return Condition(self.field, self.clause, self.values)

    def endswith(self, other):
        self.clause = f"{self.field} LIKE ?"
        self.values = [f"%{other}"]
        return Condition(self.field, self.clause, self.values)

    def substring(self, other):
        self.clause = f"{self.field} LIKE ?"
        self.values = [f"%{other}%"]
        return self.clause, self.values

    def anyof(self, *values):
        self.clause = f"{self.field} IN ({', '.join("?" * len(values))})"
        self.values = list(values)
        return Condition(self.field, self.clause, self.values)

    def noneof(self, *values):
        self.clause = f"{self.field} NOT IN ({', '.join('?' * len(values))})"
        self.values = list(values)
        return Condition(self.field, self.clause, self.values)

    def between(self, start, end):
        self.clause = f"{self.field} BETWEEN ? AND ?"
        self.values = [start, end]
        return Condition(self.field, self.clause, self.values)

    def isnull(self):
        self.clause = f"{self.field} IS NULL"
        self.values = []
        return Condition(self.field, self.clause, self.values)

    def notnull(self):
        self.clause = f"{self.field} IS NOT NULL"
        self.values = []
        return Condition(self.field, self.clause, self.values)

    def __and__(self, other):
        self.field = f"{self.field}&{other.field}"
        combined = f"({self.clause} AND {other.clause})"
        combined_values = self.values + other.values
        return Condition(self.field, combined, combined_values)

    def __or__(self, other):
        self.field = f"{self.field}|{other.field}"
        combined = f"({self.clause} OR {other.clause})"
        combined_values = self.values + other.values
        return Condition(self.field, combined, combined_values)

    def __repr__(self):
        return f"Condition({self.field})"


def cond(field: str):
    """
    Creates a condition object for a given field.

    Args:
        field (str): The name of the field.

    Returns:
        Condition: A condition object for the specified field.
    """
    return Condition(field)


class _Select:
    """
    A class representing a SQL SELECT statement.
    """

    def __init__(
        self,
        *fields: str,
        source: "Collection",
        distinct: bool = False,
        limit: int = 0,
    ):
        self.source = source
        self.sql = ""
        self.limit = limit
        if distinct:
            self.sql = "SELECT DISTINCT"
            if len(fields) > 0:
                self.sql += f" {', '.join(fields)} "
            else:
                self.sql += " * "
        elif len(fields) > 0:
            self.sql = f"SELECT {', '.join(fields)}"
        else:
            self.sql = "SELECT *"
        self.sql += f" FROM {self.source.name}"

    def where(self, condition: Condition) -> List[Dict[str, Any]]:
        """
        Set the source collection for the SELECT statement.

        Args:
            condition (Condition): The condition to filter the results.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the filtered results.
        """
        sql = self.sql + " WHERE " + condition.clause
        if self.limit:
            sql += f" LIMIT {self.limit}"
        self.source.cursor.execute(sql, condition.values)
        return [
            dict(zip([column[0] for column in self.source.cursor.description], row))
            for row in self.source.cursor.fetchall()
        ]
