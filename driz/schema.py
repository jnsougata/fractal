from .converter import as_sql_type


class Column:
    """
    A class representing a field in the database schema.
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
        self.fields = list(fields)

    def add_field(self, field: Column):
        """
        Adds a fields to the schema.
        Args:
            field (Column): The field to add to the schema.
        """
        self.fields.append(field)
