# -*- coding: utf-8 -*-

from __future__ import absolute_import

from processr.compat import reduce
from functools import partial


##############################################################
#                 Field transformers & utils                 #
##############################################################

def apply_default(value, default):
    return value if value is not None else default


def apply_map(fun):
    """
    Restituisce una funzione che trasforma gli elementi di una sequenza in modo
    lazy usando la fun fornita
    """
    def _map(sequence):
        return (fun(item) for item in sequence)
    return _map


def apply_filter(fun):
    """
    Restituisce una funzione che filtra in modo lazy gli elementi di una
    sequenza
    """
    def _filter(sequence):
        return (item for item in sequence if fun(item))
    return _filter


##############################################################
#                     Dict transformers                      #
##############################################################

def flatten(row, source_key, destination_keys):
    """
    Convert a list of dicts (identified by the source_key key in the input row) in a dict containing
    (destination_key, list) items.

    # Example
    row = {
        'doc_key': [
            {
                'sub_key_1': 1,
                'sub_key_2': 2
            },
            {
                'sub_key_1': 3
                'sub_key_2': 4
            }
        ]
    }

    row = flatten(row, 'doc_key', ['sub_key_1', 'sub_key_2'])

    output = {
        'sub_key_1': [1, 3],
        'sub_key_2': [2, 4],
    }
    """
    subdocuments = row.pop(source_key, [])

    def zip_subdocuments(key):
        zipped_value = (subdocument.get(key, None) for subdocument in subdocuments)
        return [value for value in zipped_value if value is not None]

    flatten_fields = [(key, zip_subdocuments(key)) for key in destination_keys]
    return dict(row.items() + flatten_fields)


def copy_value(row, source_key, destination_key, default=None):
    return set_value(row, destination_key, get_value(row, source_key, default))


def set_value_if(row, key, value, func):
    """
    Add (or replace) a field to a row only if the result of `func` is True for
    the computed value.
    Value could be a plain value or a callable. In the latter case,
    it will be called (with row as an argument) to build the final value.
    """
    try:
        # Value could be a callable
        value = value(row)
    except TypeError:
        pass

    if func(value):
        row[key] = value

    return row


"""
Same as set_value_if, but without the `if`. It adds the value, no matter what
its value is.
"""
set_value = partial(set_value_if, func=lambda value: True)


def get_value(row, source_key, default=None):
    """
    Estrae un valore dal documento. Supporta documenti innestati (usare il .
    per separare le chiavi).
    """
    try:
        value = reduce(lambda value, key: value[key], source_key.split('.'), row)
    except KeyError:
        value = default
    return value


def passthrough_on_exception(*exceptions):
    """
    Wrap a row transformer, catching exceptions throwed by it.
    If the exception is among the ones specified, it return the input row value.
    """
    def wrapper(f):
        def wrapped(arg):
            try:
                return f(arg)
            except exceptions:
                return arg
        return wrapped
    return wrapper
