from datetime import datetime
from typing import Any, Dict, Optional, Tuple

from .converter import as_sql_type
from .errors import FieldNotFound

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


class Field:
    """
    A class representing a field in the database schema.

    Args:
        name (str): The name of the field.
        dtype (Type): The data type of the field.
        nullable (bool): Whether the field can be null. Defaults to True.
        default (Any): The default value for the field. Defaults to None.
        unique (bool): Whether the field is unique. Defaults to False.
        check (Optional[str]): A check constraint for the field. Defaults to None.
        ref_collection (Optional[str]): The name of the collection for a foreign key. Defaults to None.
        ref_field (Optional[str]): The name of the field for a foreign key. Defaults to None.

    Attributes:
        name (str): The name of the field.
        sql_type (str): The SQL type of the field.
        * constraints (Tuple[str]): The constraints for the field.
    """

    def __init__(
        self,
        name: str,
        dtype: type,
        *,
        nullable: bool = True,
        default: Any = None,
        unique: bool = False,
        check: Optional[str] = None,
        ref_collection: Optional[str] = None,
        ref_field: Optional[str] = None,
    ):
        self.name = name
        self.sql_type = str(as_sql_type(dtype))
        self.constraints = ""
        if unique:
            self.constraints += "UNIQUE "
        if not nullable and not unique:
            self.constraints += "NOT NULL "
        if default is not None:
            self.constraints += f"DEFAULT {default} "
        if check:
            self.constraints += f"CHECK ({check}) "
        if ref_collection and ref_field:
            self.constraints += (
                f"REFERENCES {ref_collection}({ref_field}) ON DELETE CASCADE "
            )

class Schema:
    """
    A class representing the schema of a database.

    Attributes:
        collection (str): The name of the collection.
        fields (Dict[str, Field]): The fields in the schema.
    """

    def __init__(self, *fields: Field):
        """
        Initializes a Schema instance.

        Args:
            *fields (Tuple[Field]): The fields in the schema.
        """
        self.collection = None
        primary = Field("key", str)
        primary.constraints = "PRIMARY KEY " + primary.constraints
        timestamp = Field("timestamp", datetime, nullable=False)
        self.fields = {
            primary.name: primary,
            timestamp.name: timestamp,
        }
        for field in fields:
            self.fields[field.name] = field

    def append(self, *fields: Field):
        """
        Adds a field to the schema.

        Args:
            *fields (tuple[Field]): The fields to be added to the schema
        """
        for field in fields:
            self.fields[field.name] = field

    def resolve_field_type(self, field: str) -> str:
        """
        Retrieves the data type of field in the schema.

        Args:
            field (str): The name of the column.
        """
        f = self.fields.get(field)
        if not f:
            raise FieldNotFound(f"Field '{field}' not found in schema.")
        return f.sql_type
