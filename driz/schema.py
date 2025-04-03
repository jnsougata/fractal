from .converter import as_sql_type
from .errors import FieldNotFound
from datetime import datetime

from typing import Tuple, List, Any, Optional

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
            self.constraints += f"REFERENCES {ref_collection}({ref_field}) "


class Schema:
    """
    A class representing the schema of a database.

    Attributes:
        collection (str): The name of the collection.
        fields (List[Field]): The fields in the schema.

    Args:
        *fields (Tuple[Field]): The fields in the schema.
    """

    def __init__(self, *fields: Field):
        """
        Initializes a Schema instance.
        """
        self.collection = None
        primary = Field("key", str)
        primary.constraints = "PRIMARY KEY " + primary.constraints
        timestamp = Field("timestamp", datetime, nullable=False)
        self.fields  = [primary, timestamp]  # type: ignore
        self.fields.extend(fields)  # type: ignore


    def append(self, *fields: Field):
        """
        Adds a field to the schema.

        Args:
            *fields (tuple[Field]): The fields to be added to the schema
        """
        self.fields.extend(fields)  # type: ignore

    def resolve_field_type(self, field: str) -> str:
        """
        Retrieves the data type of field in the schema.

        Args:
            field (str): The name of the column.
        """
        for c in self.fields:
            if c.name == field:
                return c.sql_type
        raise FieldNotFound(f"Field '{field}' not found in schema.")
