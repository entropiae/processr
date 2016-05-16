# -*- coding: utf-8 -*-

from processr.processr import process


def test_rename():
    provided_input = {'the_answer': 42}
    expected_output = {'the_answer_to_the_ultimate_question': 42}
    pipeline = [
        ('rename_keys', {'the_answer': 'the_answer_to_the_ultimate_question'})
    ]

    output = process(provided_input, pipeline)
    assert output == expected_output


def test_rename_revert():
    provided_input = {'the_answer': 42}
    pipeline = [
        ('rename_keys', {'the_answer': 'the_answer_to_the_ultimate_question'}),
        ('rename_keys', {'the_answer_to_the_ultimate_question': 'the_answer'})
    ]

    output = process(provided_input, pipeline)
    assert output == provided_input
