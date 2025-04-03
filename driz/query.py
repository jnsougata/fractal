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

def contains(column: str, value: str) -> str:
    return f"{column} LIKE '%{value}%'"

def startswith(column: str, prefix: str) -> str:
    return f"{column} LIKE '{prefix}%'"

def endswith(column: str, suffix: str) -> str:
    return f"{column} LIKE '%{suffix}'"

def equals(column: str, value) -> str:
    if isinstance(value, (int, float)):
        return f"{column} = {value}"
    return f"{column} LIKE '{value}'"

def anyof(column: str, *values: Any) -> str:
    v = []
    for value in values:
        if isinstance(value, str):
            v.append(f"'{value}'")
        else:
            v.append(str(value))
    values_str = ", ".join(f"{str(value)}" for value in v)
    return f"{column} IN ({values_str})"

def noneof(column: str, *values: Any) -> str:
    v = []
    for value in values:
        if isinstance(value, str):
            v.append(f"'{value}'")
        else:
            v.append(str(value))
    values_str = ", ".join(f"{str(value)}" for value in v)
    return f"{column} NOT IN ({values_str})"

def between(column: str, start: Union[int, float], end: Union[int, float]) -> str:
    return f"{column} BETWEEN {start} AND {end}"

def isnull(column: str) -> str:
    return f"{column} IS NULL"

def gt(column: str, value: Union[int, float]) -> str:
    return f"{column} > {value}"
def gte(column: str, value: Union[int, float]) -> str:
    return f"{column} >= {value}"
def lt(column: str, value: Union[int, float]) -> str:
    return f"{column} < {value}"
def lte(column: str, value: Union[int, float]) -> str:
    return f"{column} <= {value}"

if __name__ == "__main__":
    print(startswith("name", "John"))  # Output: name LIKE 'John%'
    print(endswith("name", "Doe"))  # Output: name LIKE '%Doe'
    print(contains("name", "John"))  # Output: name LIKE '%John%'
    print(equals("name", "John Doe"))  # Output: name = 'John Doe'
    print(anyof("name", ["John Doe", "Jane Doe"]))  # Output: name IN ('John Doe', 'Jane Doe')
    print(between("age", 18, 30))  # Output: age BETWEEN '18' AND '30'