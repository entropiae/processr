# -*- coding: utf-8 -*-
from processr.processr import process, _field_transform, _dict_transform


def test_field_transform():
    provided_input = {'the_answer': 42}
    expected_output = {'the_answer': '43'}

    output = _field_transform(
        {'the_answer': [lambda value: value + 1, str]},
        provided_input
    )
    assert output == expected_output


def test_field_transform_extra_values():
    provided_input = {'the_answer': 42, 'not_the_answer': 43}
    expected_output = {'the_answer': '43', 'not_the_answer': 43}

    output = _field_transform(
        {'the_answer': [lambda value: value + 1, str]},
        provided_input
    )
    assert output == expected_output


def test_dict_transform():
    provided_input = {'the_answer': 42}
    expected_output = {'the_answer': 42, 'copy_of_the_answer': 42}

    def add_field(d):
        d['copy_of_the_answer'] = 42
        return d

    output = _dict_transform([add_field], provided_input)
    assert output == expected_output
