"""
FractalDB
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A fast lightweight k-v storage for hobbyists.

:copyright: (c) 2025-present Sougata Jana
:license: MIT, see LICENSE for more details.
"""

__title__ = "fractal"
__license__ = "MIT"
__copyright__ = "Copyright 2025-present Sougata Jana"
__author__ = "Sougata Jana"
__version__ = "0.0.1"


from .client import DB
from .converter import *
from .query import *
from .schema import *
