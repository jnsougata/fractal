"""
driz.query
~~~~~~~~~~~~~~~~~~~~~

A module containing functions for building SQL-like query conditions.

:copyright: (c) 2025-present Sougata Jana
:license: MIT, see LICENSE for more details.
"""

from typing import Any, Union

__all__ = [
    "negate",
    "both",
    "either",
    "contains",
    "startswith",
    "endswith",
    "equals",
    "anyof",
    "noneof",
    "between",
    "isnull",
    "gt",
    "gte",
    "lt",
    "lte",
]


def negate(condition: str) -> str:
    return f"NOT {condition}"


def both(c1: str, c2: str) -> str:
    return f"{c1} AND {c2}"


def either(c1: str, c2: str) -> str:
    return f"{c1} OR {c2}"


def contains(field: str, value: str) -> str:
    return f"{field} LIKE '%{value}%'"


def startswith(field: str, prefix: str) -> str:
    return f"{field} LIKE '{prefix}%'"


def endswith(field: str, suffix: str) -> str:
    return f"{field} LIKE '%{suffix}'"


def equals(field: str, value) -> str:
    if isinstance(value, (int, float)):
        return f"{field} = {value}"
    return f"{field} LIKE '{value}'"


def anyof(field: str, *values: Any) -> str:
    v = []
    for value in values:
        if isinstance(value, str):
            v.append(f"'{value}'")
        else:
            v.append(str(value))
    values_str = ", ".join(f"'{str(value)}'" for value in values)
    return f"{field} IN ({values_str})"


def noneof(field: str, *values: Any) -> str:
    v = []
    for value in values:
        if isinstance(value, str):
            v.append(f"'{value}'")
        else:
            v.append(str(value))
    values_str = ", ".join(f"{str(value)}" for value in v)
    return f"{field} NOT IN ({values_str})"


def between(field: str, start: Union[int, float], end: Union[int, float]) -> str:
    return f"{field} BETWEEN {start} AND {end}"


def isnull(field: str) -> str:
    return f"{field} IS NULL"


def gt(field: str, value: Union[int, float]) -> str:
    return f"{field} > {value}"


def gte(field: str, value: Union[int, float]) -> str:
    return f"{field} >= {value}"


def lt(field: str, value: Union[int, float]) -> str:
    return f"{field} < {value}"


def lte(field: str, value: Union[int, float]) -> str:
    return f"{field} <= {value}"


if __name__ == "__main__":
    print(startswith("name", "John"))  # Output: name LIKE 'John%'
    print(endswith("name", "Doe"))  # Output: name LIKE '%Doe'
    print(contains("name", "John"))  # Output: name LIKE '%John%'
    print(equals("name", "John Doe"))  # Output: name = 'John Doe'
    print(
        anyof("name", "John Doe", "Jane Doe")
    )  # Output: name IN ('John Doe', 'Jane Doe')
    print(between("age", 18, 30))  # Output: age BETWEEN '18' AND '30'
