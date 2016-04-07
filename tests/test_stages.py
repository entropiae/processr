# -*- coding: utf-8 -*-

from processr.processr import _rename_keys, _project

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


