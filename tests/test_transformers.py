# -*- coding: utf-8 -*-

import pytest

from processr.transformers import set_value, get_value, copy_value, copy_value_strict, passthrough_on_exception


class DummyException(Exception):
    pass


def raise_dummy(*args, **kwargs):
    raise DummyException


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

    with pytest.raises(DummyException):
        set_value(
            provided_input,
            'the_answer',
            raise_dummy
        )


@pytest.mark.skip(reason='private method')
def test_get_value():
    provided_input = {'the_answer': 42}
    expected_output = 42

    output = get_value(provided_input, ['the_answer'])
    assert output == expected_output


@pytest.mark.skip(reason='private method')
def test_get_nested_value():
    provided_input = {'the': {'answer': 42}}
    expected_output = 42

    output = get_value(provided_input, ['the', 'answer'])
    assert output == expected_output


@pytest.mark.skip(reason='private method')
def test_get_value_ko():
    provided_input = {'not_the_answer': 43}

    with pytest.raises(KeyError):
        get_value(provided_input, ['the_answer'])


def test_copy_value():
    provided_input = {'the_answer': 42}
    expected_output = {'the_answer': 42, 'another_time_the_answer': 42}

    output = copy_value(
        provided_input,
        ['the_answer'],
        'another_time_the_answer'
    )
    assert output == expected_output


def test_copy_value_default():
    provided_input = {'the_answer': 42}
    expected_output = {'the_answer': 42, 'not_the_answer': 43}

    output = copy_value(
        provided_input,
        ['wrong_answer'],
        'not_the_answer',
        43
    )
    assert output == expected_output


def test_copy_value_strict():
    provided_input = {'the_answer': 42}

    with pytest.raises(KeyError):
        copy_value_strict(
            provided_input,
            ['wrong_answer'],
            'not_the_answer',
        )


@passthrough_on_exception(DummyException)
def wrapped_raiser(*args, **kwargs):
    raise DummyException


def test_passthrough():
    input = {'the_answer': 42}

    output = wrapped_raiser(input)
    assert input == output


