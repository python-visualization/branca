# -*- coding: utf-8 -*-

from __future__ import absolute_import

import branca.colormap as colormap
import branca.element as element

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


__all__ = [
    'colormap',
    'element',
    ]
