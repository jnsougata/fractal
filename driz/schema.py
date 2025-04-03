from .converter import as_sql_type
from .errors import ColumnNotFound

class Column:
    """
    A class representing a column header in the database schema.
    """

    def __init__(
        self,
        name: str,
        dtype: type,
        *constraints: str,
    ):
        """
        Initializes a Field instance.

        Args:
            name (str): The name of the field.
            dtype (Type): The data type of the field.
        """
        self.name = name
        self.sql_type = str(as_sql_type(dtype))
        self.constraints = list(constraints)


class Schema:
    """
    A class representing the schema of a database.
    """

    def __init__(self, *fields: Column):
        """
        Initializes a Schema instance.

        Args:
            collection (str): The name of the collection.
        """
        self.collection = None
        self.columns = list(fields)

    def add_column(self, field: Column):
        """
        Adds a fields to the schema.
        Args:
            field (Column): The field to add to the schema.
        """
        self.columns.append(field)

    def get_column_type(self, column: str) -> str:
        """
        Returns the SQL type of column in the schema.

        Args:
            column (str): The name of the column.
        """
        for c in self.columns:
            if c.name == column:
                return c.sql_type
        raise ColumnNotFound(f"Column '{column}' not found in schema.")
