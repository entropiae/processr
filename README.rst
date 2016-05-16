******************************
processr
******************************


.. image:: https://img.shields.io/travis/entropiae/processr.svg
    :target: https://travis-ci.org/entropiae/processr
    :alt: Travis-CI


processr provides a way to apply processing pipelines (expressed as list/dict/tuples) to Python dicts.

Example
=======
The following snippet will increment the value for the key `the_answer` and then change its key to `not_the_answer`.

.. code-block:: python

    >>> from processr.processr import process
    >>> from processr.transformers import set_value
    >>> input_dict = {'the_answer': 42}

    >>> pipeline = [
    ...   ('transform_values', {'the_answer': lambda value: value + 1}),
    ...   ('rename_keys', {'the_answer': 'not_the_answer'})
    ... ]
    ... process(input_dict, pipeline)
    {'the_answer': 43}


Stages description
========================
TODO

WIP. If you're interested, reach me on `twitter <https://twitter.com/entropiae>`_.
