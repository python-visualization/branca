# -*- coding: utf-8 -*-

from __future__ import absolute_import

import sys

import branca.colormap as colormap
import branca.element as element

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

if sys.version_info < (3, 0):
    raise ImportError(
        """You are running branca {} on Python 2

    branca 0.4 and above are no longer compatible with Python 2, but somehow
    you got this version anyway. Make sure you have pip >= 9.0 to avoid this
    kind of issue, as well as setuptools >= 24.2:

     $ pip install pip setuptools --upgrade

    Your choices:

    - Upgrade to Python 3.

    - Install an older version of branca:

     $ pip install 'branca<0.4.0'

    """.format(__version__))  # noqa


__all__ = [
    'colormap',
    'element',
    ]
