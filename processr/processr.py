# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
from processr.compat import reduce, abc, NullHandler

# initialize log & set default logging handler
# to avoid 'No handler found' warnings.
log = logging.getLogger(__name__)
log.addHandler(NullHandler())


##############################################################
#                           Stages                           #
##############################################################


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


def transform_values(stage_opts, d):
    """
    Return a new dictionary whose values are taken from `d` and processed
    using the list of callable having the same key in `stage_opts`.
    Values with no specified transformers are copied untouched.

    >>> transform_values({'the_answer': [sum, str]}, {'the_answer': [41, 1]})
    {'the_answer': '42'}

    :param stage_opts: a dictionary containing key -> list of callables
    :param d: the input dictionary
    :return: a dictionary
    """
    return dict(
        (key, process_value(value, stage_opts.get(key, [])))
        for key, value in d.items()
    )


def transform_dict(stage_opts, d):
    """
    Return a new dictionary built applying all callable in `opts` to `d`.

    >>> reverse_dict = lambda d: dict((v, k) for k, v in d.items())
    >>> transform_dict([reverse_dict], {'the_answer': 42})
    {42: 'the_answer'}

    :param stage_opts: a list of callable to apply to the input dictionary
    :param d: the input dictionary
    :return: a dictionary
    """
    return process_value(d, stage_opts)


# TODO: aim for a better name
class Stages(dict):

    _default_stages = {
        'project_dict': project_dict,
        'rename_keys': rename_keys,
        'transform_values': transform_values,
        'transform_dict': transform_dict
    }

    def __init__(self, add_default_stages=True, **kwargs):
        super(Stages, self).__init__(**kwargs)

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


def process(d, pipeline, stage_definitions=Stages()):
    """
    Process a dictionary according to the given pipeline.

    :param d: the dictionary to process
    :param pipeline: the processing pipeline
    :param stage_definitions:
    :return: a dictionary
    """
    def process_stage(d, stage):
        stage_name = stage['stage']
        handler = stage_definitions[stage_name]
        return handler(stage['opts'], d)

    return reduce(process_stage, pipeline, d)
