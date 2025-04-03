from .converter import as_sql_type
from .errors import FieldNotFound

from typing import Tuple, List

class Field:
    """
    A class representing a field in the database schema.

    Args:
        name (str): The name of the field.
        dtype (Type): The data type of the field.
        constraints (str): Optional constraints for the field (e.g., "NOT NULL", "UNIQUE").

    Attributes:
        name (str): The name of the field.
        sql_type (str): The SQL type of the field.
        * constraints (Tuple[str]): The constraints for the field.
    """

    def __init__(self, name: str, dtype: type, *constraints: str):
        self.name = name
        self.sql_type = str(as_sql_type(dtype))
        self.constraints = constraints  # noqa


class Schema:
    """
    A class representing the schema of a database.

    Attributes:
        collection (str): The name of the collection.
        fields (List[Field]): The fields in the schema.

    Args:
        *fields (Field): The fields in the schema.
    """

    def __init__(self, *fields: Field):
        """
        Initializes a Schema instance.

        Args:
            collection (str): The name of the collection.
        """
        self.collection = None
        self.fields: List[Field] = list(fields)  # noqa

    def append(self, *fields: Field):
        """
        Adds a field to the schema.

        Args:
            *fields (Field): The fields to be added to the schema
        """
        self.fields.extend(fields)

    def resolve_field_type(self, field: str) -> str:
        """
        Retrieves the data type of a field in the schema.

        Args:
            field (str): The name of the column.
        """
        for c in self.fields:
            if c.name == field:
                return c.sql_type
        raise FieldNotFound(f"Field '{field}' not found in schema.")
