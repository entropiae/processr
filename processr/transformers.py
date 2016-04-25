# -*- coding: utf-8 -*-

from __future__ import absolute_import

from processr.compat import reduce

from processr.compat import abc


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

def set_value(d, key, value, func=lambda _: True):
    """
    Add (or replace) a field to a dict only if the result of `func` is True
    for the computed value.
    Value could be a plain value or a callable. In the latter case,
    it will be called (with row as an argument) to build the real value.

    Add it to your pipeline like:
    (
        set_value,
        {
            'key': 'the_answer',
            'value': 42,  # or something like lambda d: 42
            'func': lambda x: True  # optional
        }
    )

    :param d: the input dictionary
    :param key: the key of the value to set
    :param value: the value to set; could be a callable
    :param func: an optional boolean function that will be called
    on the value to check if should be added to the dictionary
    :return: a dictionary
    """

    if isinstance(value, abc.Callable):
        # Q: Why are you using LBYL instead of EAFP?
        # A: Catching the TypeError raised by value() when its not
        # a callable will swallow potential exceptions raised
        # by the code inside it when it is a callable.
        value = value(d)

    if func(value):
        d[key] = value

    return d


def get_value(d, keys):
    """
    Retrieve a value from a dict. Raise KeyError if the key isn't found.
    `keys` is an iterable of key, to support nested dicts.
    """
    return reduce(lambda sub_d, key: sub_d[key], keys, d)


def copy_value(d, source_key, destination_key, default=None):
    """
    Copy a value from an item of a dict to another item. Source
    item could be a nested dict. If the source value isn't found
    `default` is used.
    :param d: the input dictionary
    :param source_key: an iterable of keys
    :param destination_key: the key of the new item
    :param default: the value to set if `source_keys` isn't in the dictionary
    :return: a dictionary
    """
    try:
        value = get_value(d, source_key)
    except KeyError:
        value = default

    return set_value(d, destination_key, value)


def copy_value_strict(d, source_key, destination_key):
    """
    Like copy_value, but raise a KeyError if the value isn't found.
    """
    return set_value(d, destination_key, get_value(d, source_key))


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
