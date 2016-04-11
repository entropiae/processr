# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
from itertools import chain

from processr.compat import reduce, abc, NullHandler

# initialize log & set default logging handler
# to avoid 'No handler found' warnings.
log = logging.getLogger(__name__)
log.addHandler(NullHandler())


##############################################################
#                           Stages                           #
##############################################################


def rename_keys(d, stage_opts):
    """
    Returns a dictionary composed by items from `d`; when a key is found
    in `opts`, the corresponding value is used as key in the new dictionary.

    >>> rename_keys({'key': 42}, {'key': 'new_key'})
    {'new_key': 42}

    :param d: the input dictionary
    :param stage_opts: a mapping used to translate old_key -> new_key
    :return: a dictionary
    """
    return dict((stage_opts.get(k, k), v) for k, v in d.items())


def project_dict(d, stage_opts):
    """
    Returns a dictionary composed by items from `d` whose keys are
    in `opts` collection.
    If `opts`contains a key which is not in `d` a `KeyError` is raised.

    >>> project_dict({'a': 1, 'b': 2}, ('a', ))
    {'a': 1}

    will be maintained in the returned dict.
    :param d: the input dictionary
    :param stage_opts: a collection containing the key which
    :return: a dictionary
    """
    return dict((k, d[k]) for k in stage_opts)


def transform_values(d, stage_opts):
    """
    Return a new dictionary whose values are taken from `d` and processed
    using the list of callable having the same key in `stage_opts`.
    Values with no specified transformers are copied untouched.

    >>> transform_values({'the_answer': [41, 1]}, {'the_answer': [sum, str]})
    {'the_answer': '42'}

    :param d: the input dictionary
    :param stage_opts: a dictionary containing key -> list of callables
    :return: a dictionary
    """
    return dict(
        (key, process_value(value, stage_opts.get(key, [])))
        for key, value in d.items()
    )


def transform_values_strict(d, stage_opts):
    """
    Like `transform_values`, but raise a `KeyError` if a key from stage_opts
    isn't found in d.
    :param d: the input dictionary
    :param stage_opts: a dictionary containing key -> list of callables
    :return: a dictionary
    """

    unchanged_items = (
        (key, value)
        for key, value in d.items()
        if key not in stage_opts
    )

    processed_items = (
        (key, process_value(d[key], opts))
        for key, opts in stage_opts.items()
    )

    return dict(
        chain(unchanged_items, processed_items)
    )


def transform_dict(d, stage_opts):
    """
    Return a new dictionary built applying all callable in `opts` to `d`.

    >>> reverse_dict = lambda d: dict((v, k) for k, v in d.items())
    >>> transform_dict({'the_answer': 42}, [reverse_dict])
    {42: 'the_answer'}

    :param d: the input dictionary
    :param stage_opts: a list of callable to apply to the input dictionary
    :return: a dictionary
    """
    return process_value(d, stage_opts)


class StageDefinitions(dict):
    """
    Provides a way to get a stage handler by its name, and a way
    to trivially add custom stages.

    :param add_default_stages: add the 4 default stage handlers
    """

    _default_stages = {
        'project_dict': project_dict,
        'rename_keys': rename_keys,
        'transform_values': transform_values,
        'transform_dict': transform_dict,
        'transform_values_strict': transform_values_strict
    }

    def __init__(self, add_default_stages=True):

        super(StageDefinitions, self).__init__()

        if add_default_stages:
            for stage_name, stage_handler in self._default_stages.items():
                self[stage_name] = [stage_handler]


##############################################################
#                     Process all the things!                #
##############################################################

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
        f, kwargs = fs
        log.debug(
            {'transformer': f, 'kwargs': kwargs, 'input': value}
        )
        return_value = f(value, **kwargs)
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


def process(d, pipeline, stage_definitions=StageDefinitions()):
    """
    Process a dictionary according to the given pipeline, using
    the stage handlers defined in stage_definitions.

    :param d: the dictionary to process
    :param pipeline: the processing pipeline
    :param stage_definitions: a (stage_name, stage_handler) mapping
    :return: a dictionary
    """
    def process_stage(d, stage):
        stage_name, stage_option = stage
        try:
            handler = stage_definitions[stage_name]
        except KeyError:
            raise
        return handler(d, stage_option)

    return reduce(process_stage, pipeline, d)
