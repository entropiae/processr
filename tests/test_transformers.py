# -*- coding: utf-8 -*-

import pytest

from processr.transformers import set_value


def test_set_value():
    provided_input = {}
    expected_output = {'the_answer': 42}

    output = set_value(
        provided_input,
        'the_answer',
        42
    )
    assert output == expected_output


def test_set_value_callable():
    provided_input = {}
    expected_output = {'the_answer': 42}

    output = set_value(
        provided_input,
        'the_answer',
        lambda _: 42,
    )
    assert output == expected_output


def test_set_value_if():
    provided_input = {}
    expected_output = {'the_answer': 42}

    output = set_value(
        provided_input,
        'the_answer',
        42,
        lambda value: value % 2 == 0
    )
    assert output == expected_output


def test_set_value_if_not():
    provided_input = {}
    expected_output = {}

    output = set_value(
        provided_input,
        'the_answer',
        42,
        lambda value: value == 6 * 9
    )
    assert output == expected_output


def test_set_value_if_exception_bubbling():
    provided_input = {}

    def raise_exc(_):
        raise TypeError

    with pytest.raises(TypeError):
        set_value(
            provided_input,
            'the_answer',
            raise_exc
        )
