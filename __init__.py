"""
QTask-Py
~~~~~~~~

A Redis-based task queue library for Python.
"""

__version__ = "0.1.0"
__author__ = "Rafael Jose Garcia Suarez"
__email__ = "rafaeljosegarciasuarez@gmail.com"

from core.subscriber import Subscriber
from core.publisher import Publisher

__all__ = [
    'Subscriber',
    'Publisher',
    '__version__',
    '__author__',
    '__email__'
]
