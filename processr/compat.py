# -*- coding: utf-8 -*-

try:
    from functools import reduce
except ImportError:
    reduce = reduce

try:
    import collections.abc as abc
except ImportError:
    import collections as abc

import logging
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

__all__ = ['reduce', 'abc', 'NullHandler']
