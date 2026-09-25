"""Compute the Brillouin zone of a crystal.

This subpackage needs the optional ``scipy`` dependency, installed with
``pip install seekpath[bz]``.
"""

from .brillouinzone import BZ, get_BZ

__all__ = ('BZ', 'get_BZ')
