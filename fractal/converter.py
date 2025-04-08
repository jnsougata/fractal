from datetime import date, datetime, time, timedelta

__all__ = [
    "date",
    "datetime",
    "time",
    "timedelta",
    "as_sql_type",
    "from_sql_type",
]

_SQLEquivalentTypes = {
    int: "INTEGER",
    float: "REAL",
    bool: "BOOLEAN",
    str: "TEXT",
    bytes: "BLOB",
    datetime: "DATETIME",
    date: "DATE",
    time: "TIME",
    timedelta: "TIME",
    None: "NULL",
}


def as_sql_type(dtype: type) -> str:
    return _SQLEquivalentTypes.get(dtype, "UNKNOWN")  # noqa


def from_sql_type(sql_type: str) -> type:
    for py_type, sql in _SQLEquivalentTypes.items():
        if sql == sql_type:
            return py_type
    raise ValueError(f"Unknown SQL type: {sql_type}")
