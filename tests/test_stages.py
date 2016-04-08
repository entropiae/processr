# -*- coding: utf-8 -*-

from processr.processr import _rename_keys, _project, _field_transform, _dict_transform

import pytest


def test_rename_keys():
    provided_input = {'the_answer': 42}
    opts = {'the_answer': 'the_universe_and_everything'}
    expected_output = {'the_universe_and_everything': 42}

    output = _rename_keys(opts, provided_input)
    assert output == expected_output


def test_rename_keys_extra_fields():
    provided_input = {'the_answer': 42, 'not_the_answer': 43}
    opts = {'the_answer': 'the_universe_and_everything'}
    expected_output = {'the_universe_and_everything': 42, 'not_the_answer': 43}

    output = _rename_keys(opts, provided_input)
    assert output == expected_output


def test_project():
    provided_input = {'the_answer': 42, 'not_the_answer': 43}
    opts = ('the_answer', )
    expected_output = {'the_answer': 42}

    output = _project(opts, provided_input)
    assert output == expected_output


def test_project_extra_fields():
    provided_input = {'the_answer': 42, 'not_the_answer': 43}
    opts = ('the_answer', 'the_universe')

    with pytest.raises(KeyError):
        _project(opts, provided_input)


def test_transform_fields():
    provided_input = {'not_the_answer': [9, 9, 9, 9, 9, 9]}
    opts = {'not_the_answer': [sum, str]}

    # I always thought something was fundamentally wrong with the universe
    expected_output = {'not_the_answer': '54'}
    output = _field_transform(opts, provided_input)
    assert output == expected_output


def test_transform_fields_extra_fields():
    provided_input = {'not_the_answer': [9, 9, 9, 9, 9, 9], 'the_answer': 42}
    opts = {'not_the_answer': [sum, str]}

    expected_output = {'not_the_answer': '54', 'the_answer': 42}
    output = _field_transform(opts, provided_input)
    assert output == expected_output


def test_dict_transform():
    provided_input = {'the_answer': 42, 'not_the_answer': 43}
    ops = [lambda d: dict((v, k) for k, v in d.items())] # Invert key and value in d

    expected_output = {42: 'the_answer', 43: 'not_the_answer'}
    output = _dict_transform(ops, provided_input)
    assert output == expected_output


