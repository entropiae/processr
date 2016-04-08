# -*- coding: utf-8 -*-

from processr.processr import process_value


def test_process_simple():
    input_value = 42
    opts = str
    expected_output = '42'

    output = process_value(input_value, opts)
    assert output == expected_output


def test_process_value_list():
    input_value = [1 for _ in range(42)]
    opts = [sum, str]
    expected_output = '42'

    output = process_value(input_value, opts)
    assert output == expected_output


def test_process_value_fun_with_args():
    input_value = 41

    def sum(a, b):
        return a + b

    opts = [(sum, [], {'b': 1}), str]
    expected_output = '42'

    output = process_value(input_value, opts)
    assert output == expected_output
