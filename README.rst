=============================
quartet_output
=============================

.. image:: https://badge.fury.io/py/quartet_output.svg
    :target: https://badge.fury.io/py/quartet_output

.. image:: https://travis-ci.org/serial-lab/quartet_output.svg?branch=master
    :target: https://travis-ci.org/serial-lab/quartet_output

.. image:: https://codecov.io/gh/serial-lab/quartet_output/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/serial-lab/quartet_output

Output logic for QU4RTET supply chain messaging.

Documentation
-------------

The full documentation is at https://serial-lab.gitlab.io/quartet_output

Quickstart
----------

Install quartet_output::

    pip install quartet_output

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'quartet_output.apps.QuartetOutputConfig',
        ...
    )

Add quartet_output's URL patterns:

.. code-block:: python

    from quartet_output import urls as quartet_output_urls


    urlpatterns = [
        ...
        url(r'^', include(quartet_output_urls)),
        ...
    ]

Features
--------

* TODO

Running The Unit Tests
-------------

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

