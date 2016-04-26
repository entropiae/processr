# -*- coding: utf-8 -*-

from __future__ import absolute_import

import functools

from processr.compat import reduce

from processr.compat import abc


##############################################################
#                 Field transformers & utils                 #
##############################################################

def apply_default(default, null_values=(None, '')):
    """
    Return a functions which apply a default if value is "nullable".

    >>> default = apply_default(42)
    >>> default(None)
    42
    """
    def _apply_default(value):
        return value if value not in null_values else default
    return _apply_default


def apply_map(fun):
    """
    Return a function which lazily apply the provided
    function on an interable.

    >>> mapper = apply_map(lambda x: x + 1)
    >>> list(mapper([1, 2, 3]))
    [2, 3, 4]
    """
    def _map(iterable):
        return (fun(elem) for elem in iterable)
    return _map


def apply_filter(fun):
    """
    Return a function which lazily filter the iterable using the
    given function.

    >>> flt = apply_filter(lambda x: x % 2 == 0)
    >>> list(flt([1, 2, 3]))
    [2]
    """
    def _filter(iterable):
        return (element for element in iterable if fun(element))
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


def passthrough_on_exception(*exceptions):
    """
    Wrap a dict transformer, catching threw exception.
    If threw_exception in exceptions, return the input dict. Else,
    reraise the exception.
    """
    def wrapper(f):
        @functools.wraps(f)
        def wrapped(d):
            try:
                return f(d)
            except exceptions:
                return d
        return wrapped
    return wrapper
