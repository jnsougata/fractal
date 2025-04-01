from datetime import datetime, date, time, timedelta
from typing import Union, Type

SQLEquivalentTypes = {
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

class AsType:
    """
    A class to represent a data type of SQL equivalent types.
    """

    def __init__(self, dtype: Type[Union[int, float, bool, str, bytes, datetime, date, time, timedelta]]):
        """
        Initializes a TypeConverter instance.
        """
        self.dtype = dtype

    @classmethod
    def from_sql_type(cls, sql_type: str):
        """
        Converts a SQL type to the corresponding Python type.
        """
        for py_type, sql in SQLEquivalentTypes.items():
            if sql == sql_type:
                return cls(py_type)
        raise ValueError(f"Unknown SQL type: {sql_type}")

    def __str__(self):
        """
        Returns the string representation of the data type.
        """
        return SQLEquivalentTypes.get(self.dtype, "UNKNOWN")


if __name__ == "__main__":
    converter = AsType(int)
    print(str(converter))  # Output: INTEGER