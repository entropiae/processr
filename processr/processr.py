# -*- coding: utf-8 -*-

try:
    from functools import reduce
except ImportError:  # PY2
    reduce = reduce

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


def _rename_keys(opts, d):
    """
    Returns a dictionary composed by items from `d`; when a key is found
    in `opts`, the corresponding value is used as key in the new dictionary.

    >>> _rename_keys({'key': 'new_key'}, {'key': 42})
    {'new_key': 42}

    :param opts: a mapping used to translate old_key -> new_key
    :param d: the input dictionary
    :return: a dictionary
    """
    return dict((opts.get(k, k), v) for k, v in d.items())


def _project(opts, d):
    """
    Returns a dictionary composed by items from `d` whose keys are
    in `opts` collection.
    If `opts`contains a key which is not in `d` a `KeyError` is raised.

    >>> _project(('a', ), {'a': 1, 'b': 2})
    {'a': 1}

    :param opts: a collection containing the key which will be mantained in
    the returned dict
    :param d: the input dictionary
    :return: a dictionary
    """
    return dict((k, d[k]) for k in opts)


def _field_transform(stage_opts, d):
    """
    Return a new dictionary whose values are taken from `d` and processed
    using the list of callable having the same key in `stage_opts`.
    Values with no specified transformers are copied untouched.

    >>> _field_transform({'the_answer': [sum, str]}, {'the_answer': [41, 1]})
    {'the_answer': '42'}

    :param stage_opts: a dictionary containing key -> list of callables
    :param d: the input dictionary
    :return: a dictionary
    """
    return dict(
        (key, _process_obj(original_value, stage_opts.get(key, [])))
        for key, original_value in d.items()
    )


def _dict_transform(opts, d):
    # opts: [op_1, op_2, op_3]
    return _process_obj(d, opts)


def _process_obj(value, opts):
    return reduce(lambda x, f: f(x), opts, value)

handlers = {
    'field_transform': _field_transform,
    'dict_transform': _dict_transform,
    'rename_keys': _rename_keys,
    'project': _project
}


def process_stage(d, stage):
    stage_name = stage['stage']
    handler = handlers[stage_name]
    return handler(stage['opts'], d)


def process(d, pipeline):
    return reduce(process_stage, pipeline, d)
