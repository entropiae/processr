# -*- coding: utf-8 -*-

from processr.processr import (
    rename_keys,
    project_dict,
    transform_values,
    transform_dict,
    transform_values_strict)

import pytest


##############################################################
#                        rename_keys                         #
##############################################################

def test_rename_keys():
    d = {'the_answer': 42}
    opts = {'the_answer': 'the_universe_and_everything'}
    expected_output = {'the_universe_and_everything': 42}

    output = rename_keys(d, opts)
    assert output == expected_output


def test_rename_keys_extra_fields():
    d = {'the_answer': 42, 'not_the_answer': 43}
    opts = {'the_answer': 'the_universe_and_everything'}
    expected_output = {'the_universe_and_everything': 42, 'not_the_answer': 43}

    output = rename_keys(d, opts)
    assert output == expected_output


##############################################################
#                          project                           #
##############################################################

def test_project_dict():
    d = {'the_answer': 42, 'not_the_answer': 43}
    opts = ('the_answer', )
    expected_output = {'the_answer': 42}

    output = project_dict(d, opts)
    assert output == expected_output


def test_project_dict_extra_fields():
    d = {'the_answer': 42, 'not_the_answer': 43}
    opts = ('the_answer', 'the_universe')

    with pytest.raises(KeyError):
        project_dict(d, opts)


##############################################################
#                      transform_values                      #
##############################################################

def test_transform_values():
    d = {'not_the_answer': [9, 9, 9, 9, 9, 9]}
    opts = {'not_the_answer': [sum, str]}

    # I always thought something was fundamentally wrong with the universe
    expected_output = {'not_the_answer': '54'}
    output = transform_values(d, opts)
    assert output == expected_output


def test_transform_values_extra_fields():
    d = {'not_the_answer': [9, 9, 9, 9, 9, 9], 'the_answer': 42}
    opts = {'not_the_answer': [sum, str]}

    expected_output = {'not_the_answer': '54', 'the_answer': 42}
    output = transform_values(d, opts)
    assert output == expected_output


def test_transform_values_non_strictness():
    d = {'not_the_answer': [9, 9, 9, 9, 9, 9]}
    opts = {'the_answer': [str]}

    expected_output = {'not_the_answer': [9, 9, 9, 9, 9, 9]}
    output = transform_values(d, opts)
    assert output == expected_output


def test_transform_values_strict():
    d = {'not_the_answer': [9, 9, 9, 9, 9, 9]}
    opts = {'not_the_answer': [sum, str]}

    expected_output = {'not_the_answer': '54'}
    output = transform_values_strict(d, opts)
    assert output == expected_output


def test_transform_values_strict_ko():
    d = {'not_the_answer': [9, 9, 9, 9, 9, 9]}
    opts = {'the_answer': [str]}

    with pytest.raises(KeyError):
        transform_values_strict(d, opts)

##############################################################
#                       transform_dict                       #
##############################################################


def test_dict_transform():
    d = {'the_answer': 42, 'not_the_answer': 43}
    ops = [
        lambda d: dict((v, k) for k, v in d.items())  # Invert key and values
    ]

    expected_output = {42: 'the_answer', 43: 'not_the_answer'}
    output = transform_dict(d, ops)
    assert output == expected_output
