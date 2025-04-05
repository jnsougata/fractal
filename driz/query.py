"""
driz.query
~~~~~~~~~~~~~~~~~~~~~

A module containing functions for building SQL-like query conditions.

:copyright: (c) 2025-present Sougata Jana
:license: MIT, see LICENSE for more details.
"""

from typing import Any, Union, TYPE_CHECKING, Dict, List

if TYPE_CHECKING:
    from .collection import Collection

__all__ = ["_Select", "Where"]

class Where:
    """
    A class representing a SQL WHERE clause.
    """

    def __init__(
        self,
        select: "_Select",
        ored: bool = False,
        source: "Collection" = None,
        limit: int = 0,
    ):
        self.limit = limit
        self.source = source
        self.condition = ""
        self.ored = ored
        self.select = select

    def _join(self, condition: str):
        if self.ored:
            self.condition += f"{condition} OR "
        else:
            self.condition += f"{condition} AND "

    def equals(self, field: str, value: Any):
        if isinstance(value, (int, float)):
            self._join(f"{field} = {value}")
        else:
            self._join(f"{field} LIKE '{value}'")
        return self

    def negate(self, condition: str):
        self._join(condition)
        return self

    def anyof(self, field: str, *values: Any):
        v = []
        for value in values:
            if isinstance(value, str):
                v.append(f"'{value}'")
            else:
                v.append(str(value))
        values_str = ", ".join(v)
        self.condition += self._join(f"{field} IN ({values_str})")
        return self

    def noneof(self, field: str, *values: Any):
        v = []
        for value in values:
            if isinstance(value, str):
                v.append(f"'{value}'")
            else:
                v.append(str(value))
        values_str = ", ".join(v)
        self._join(f"{field} NOT IN ({values_str})")
        return self

    def between(self, field: str, start: Union[int, float], end: Union[int, float]):
        self._join(f"{field} BETWEEN {start} AND {end}")
        return self

    def isnull(self, field: str):
        self._join(f"{field} IS NULL")
        return self

    def gt(self, field: str, value: Union[int, float]):
        self._join(f"{field} > {value}")
        return self

    def gte(self, field: str, value: Union[int, float]):
        self._join(f"{field} >= {value}")
        return self

    def lt(self, field: str, value: Union[int, float]):
        self._join(f"{field} < {value}")
        return self

    def lte(self, field: str, value: Union[int, float]):
        self._join(f"{field} <= {value}")
        return self

    def startswith(self, field: str, prefix: str):
        self._join(f"{field} LIKE '{prefix}%'")
        return self

    def endswith(self, field: str, suffix: str):
        self._join(f"{field} LIKE '%{suffix}'")
        return self

    def substring(self, field: str, value: str):
        self._join(f"{field} LIKE '%{value}%'")
        return self

    def exec(self) -> List[Dict[str, Any]]:
        """
        Executes the WHERE clause and returns the results.
        """
        if self.condition:
            sql = (self.select.sql + " WHERE " + self.condition).strip(" AND").strip(" OR")

        else:
            sql = self.source.cursor.execute(f"SELECT * FROM {self.source.name}")
        if self.limit:
            sql += f" LIMIT {self.limit}"
        self.source.cursor.execute(sql)
        return [
            dict(zip([column[0] for column in self.source.cursor.description], row))
            for row in self.source.cursor.fetchall()
        ]

class _Select:
    """
    A class representing a SQL SELECT statement.
    """

    def __init__(
        self,
        *fields: str,
        source: "Collection",
        distinct: bool = False,
        ored: bool = False,
        limit: int = 0,
    ):
        self.source = source
        self.ored = ored
        self.sql = ""
        self.limit = limit
        if distinct:
            self.sql = "SELECT DISTINCT"
            if len(fields) > 0:
                self.sql += f" {', '.join(fields)} "
        elif len(fields) == 0:
            self.sql = "SELECT *"
        else:
            self.sql = f"SELECT {', '.join(fields)}"

        self .sql += f" FROM {source.name}"

    @property
    def where(self) -> Where:
        """
        Set the source collection for the SELECT statement.
        """
        return Where(self, ored=self.ored, source=self.source, limit=self.limit)
