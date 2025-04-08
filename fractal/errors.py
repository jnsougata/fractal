"""
fractal.errors
~~~~~~~~~~~~~~~~~~~~~

A module containing custom exceptions for the Fractal database library.

:copyright: (c) 2025-present Sougata Jana
:license: MIT, see LICENSE for more details.
"""


class CollectionNotFound(Exception):
    """Exception raised when a collection is not found in the database."""

    pass


class FieldNotFound(Exception):
    """Exception raised when a column is not found in the database."""

    pass
