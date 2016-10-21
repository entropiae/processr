******************************
processr
******************************


.. image:: https://img.shields.io/travis/entropiae/processr.svg
    :target: https://travis-ci.org/entropiae/processr
    :alt: Travis-CI


processr provides a way to apply processing pipelines (expressed as list/dict/tuples) to Python dicts.

Example
=======
The following snippet will increment the value for the key ``the_answer`` and then change its key to ``not_the_answer``.

.. code-block:: python

    >>> from processr.processr import process
    >>> from processr.transformers import set_value
    >>> input_dict = {'the_answer': 42}

    >>> pipeline = [
    ...   ('transform_values', {'the_answer': lambda value: value + 1}),
    ...   ('rename_keys', {'the_answer': 'not_the_answer'})
    ... ]
    >>> process(input_dict, pipeline)
    {'not_the_answer': 43}


processr's lingo
================
processr tr


Stages
======
In processr lingo, every kind of transformation applied to the dictionary is called a stage.
In the previous example, two different stages are involved: transform_values and rename_keys.

A set of stages is included with processr:
``rename_keys``:
``project_dict``
``transform_values`` + ``transform_values_strict``
``transform_dict``


WIP. If you're interested, reach me on `twitter <https://twitter.com/entropiae>`_.
