"""
fractal.query
~~~~~~~~~~~~~~~~~~~~~

A module containing functions for building SQL-like query conditions.

:copyright: (c) 2025-present Sougata Jana
:license: MIT, see LICENSE for more details.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Union

from .schema import Condition

if TYPE_CHECKING:
    from .collection import Collection

__all__ = ["_Select"]


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
