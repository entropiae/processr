# -*- coding: utf-8 -*-

try:
    from functools import reduce
except ImportError:
    # PY2
    pass

"""
3 stage-types:
    field_transform -> change a value of the dict, leaving the 'shape' unchanged
    dict_transform -> change multiple field at once, change the shape of the dict
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

dummy_stage = lambda x: x


def _rename_keys(opts, d):
    # opts = {old_key: new_key}
    return dict((opts[k], v) for k, v in d.items())


def _project(opts, d):
    # opts = ('key_1', 'key_2')
    return dict((k, v) for k, v in d.items() if k in opts)


def _field_transform(stage_opts, d):
    # opts: {'key': [op_1, op_2], 'key_2': [op_1. op_2]}
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








