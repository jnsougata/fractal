from datetime import date, datetime, time, timedelta

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


if __name__ == "__main__":
    converter = as_sql_type(int)
    print(str(converter))  # Output: INTEGER
