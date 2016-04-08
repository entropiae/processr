===============================
processr
===============================

.. image:: https://img.shields.io/pypi/v/processr.svg
        :target: https://pypi.python.org/pypi/processr

.. image:: https://img.shields.io/travis/entropiae/processr.svg
        :target: https://travis-ci.org/entropiae/processr

.. image:: https://readthedocs.org/projects/processr/badge/?version=latest
        :target: https://readthedocs.org/projects/processr/?badge=latest
        :alt: Documentation Status


Compose your dictionary-processing pipeline

* Documentation: https://processr.readthedocs.org.

Features
--------

4 stage-types:
    field_transform -> change a value of the dict, leaving the 'shape'
        unchanged
    dict_transform -> change multiple field at once, change the shape
        of the dict
    rename_keys -> rename the keys
    project -> keep only a subset of the dict

The pipeline will be a list of the following format
pipeline = [
    {
        'stage': 'field_transform/dict_transform/rename_keys/project',
        'opts': [...]
    }
]

* TODO

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
