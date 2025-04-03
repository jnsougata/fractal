class CollectionNotFound(Exception):
    """Exception raised when a collection is not found in the database."""

    pass

class FieldNotFound(Exception):
    """Exception raised when a column is not found in the database."""

    pass