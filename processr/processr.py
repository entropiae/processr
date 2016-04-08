# -*- coding: utf-8 -*-

try:
    from functools import reduce
except ImportError:  # PY2
    reduce = reduce

import collections.abc as abc
import logging

# Set default logging handler to avoid "No handler found" warnings.
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

log = logging.getLogger(__name__)
log.addHandler(NullHandler())


"""
4 stage-types:
    field_transform -> change a value of the dict, leaving the 'shape'
        unchanged
    dict_transform -> change multiple field at once, change the shape
        of the dict
    rename_keys -> rename the keys
    project -> keep only a subset of the dict

The pipeline will be a list of the following format
pipeline = [
    {
        'stage': 'field_transform/dict_transform/rename_keys/project',
        'opts': [...]
    }
]
"""


def rename_keys(stage_opts, d):
    """
    Returns a dictionary composed by items from `d`; when a key is found
    in `opts`, the corresponding value is used as key in the new dictionary.

    >>> rename_keys({'key': 'new_key'}, {'key': 42})
    {'new_key': 42}

    :param stage_opts: a mapping used to translate old_key -> new_key
    :param d: the input dictionary
    :return: a dictionary
    """
    return dict((stage_opts.get(k, k), v) for k, v in d.items())


def project_dict(stage_opts, d):
    """
    Returns a dictionary composed by items from `d` whose keys are
    in `opts` collection.
    If `opts`contains a key which is not in `d` a `KeyError` is raised.

    >>> project_dict(('a', ), {'a': 1, 'b': 2})
    {'a': 1}

    :param stage_opts: a collection containing the key which
    will be maintained in the returned dict.
    :param d: the input dictionary
    :return: a dictionary
    """
    return dict((k, d[k]) for k in stage_opts)


def process_values(stage_opts, d):
    """
    Return a new dictionary whose values are taken from `d` and processed
    using the list of callable having the same key in `stage_opts`.
    Values with no specified transformers are copied untouched.

    >>> process_values({'the_answer': [sum, str]}, {'the_answer': [41, 1]})
    {'the_answer': '42'}

    :param stage_opts: a dictionary containing key -> list of callables
    :param d: the input dictionary
    :return: a dictionary
    """
    return dict(
        (key, process_value(value, stage_opts.get(key, [])))
        for key, value in d.items()
    )


def process_dict(stage_opts, d):
    """
    Return a new dictionary built applying all callable in `opts` to `d`.

    >>> reverse_dict = lambda d: dict((v, k) for k, v in d.items())
    >>> process_dict([reverse_dict], {'the_answer': 42})
    {42: 'the_answer'}

    :param stage_opts: a list of callable to apply to the input dictionary
    :param d: the input dictionary
    :return: a dictionary
    """
    return process_value(d, stage_opts)


class InvalidTransformerFormat(Exception):
    pass


def process_value(value, fs):
    """
    Process a value.

    :param value: the input value to process
    :param fs: transformer(s) used to process value.
        Could be a callable, a (callable, args, kwargs) tuple
        or a list of both.
    :return: the processed value
    """
    if isinstance(fs, tuple):
        # The transformer is a function which requires extra arguments,
        # so is expressed as a (f, args, kwargs) tuple.
        f, args, kwargs = fs
        log.debug(
            {'transformer': f, 'args': args, 'kwargs': kwargs, 'input': value}
        )
        return_value = f(value, *args, **kwargs)
        log.debug({'output': return_value})
    elif isinstance(fs, abc.Iterable):
        # The transformers is actually a list of transformers.
        # Recursively call process_value to apply all of them.
        return_value = reduce(process_value, fs, value)
    elif isinstance(fs, abc.Callable):
        # Transformer is a callable w/o extra arguments.
        # Call it!
        log.debug({'transformer': fs, 'input': value})
        return_value = fs(value)
        log.debug({'output': return_value})
    else:
        raise InvalidTransformerFormat(fs)
    return return_value


handlers = {
    'field_transform': process_values,
    'dict_transform': process_dict,
    'rename_keys': rename_keys,
    'project': project_dict
}


def process_stage(d, stage):
    stage_name = stage['stage']
    handler = handlers[stage_name]
    return handler(stage['opts'], d)


def process(d, pipeline):
    return reduce(process_stage, pipeline, d)
