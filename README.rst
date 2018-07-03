=============================
quartet_output
=============================

.. image:: https://gitlab.com/serial-lab/quartet_output/badges/master/coverage.svg
   :target: https://gitlab.com/serial-lab/quartet_output/pipelines
.. image:: https://gitlab.com/serial-lab/quartet_output/badges/master/build.svg
   :target: https://gitlab.com/serial-lab/quartet_output/commits/master
.. image:: https://badge.fury.io/py/quartet_output.svg
    :target: https://badge.fury.io/py/quartet_output

Output Rules and logic for QU4RTET supply chain messaging.

Documentation
-------------

The full documentation is at https://serial-lab.gitlab.io/quartet_output

Quickstart
----------

Install quartet_output

.. code-block:: text

    pip install quartet_output

Add it to your `INSTALLED_APPS`:

.. code-block:: text

    INSTALLED_APPS = (
        ...
        'quartet_output.apps.QuartetOutputConfig',
        ...
    )

Add quartet_output's URL patterns:

.. code-block:: text

    from quartet_output import urls as quartet_output_urls


    urlpatterns = [
        ...
        url(r'^', include(quartet_output_urls)),
        ...
    ]

Features
--------

* Output determination allows you to create filters on inbound EPCIS data
  and determine which inbound EPCIS events trigger outbound business messaging.

* Define HTTP and HTTPS end points for trading partners.

* Define various authentication schemes for external end points.

* Outbound messages take advantage of the `quartet_capture` rule engine by
  creating a new outbound task for every message.  This puts every outbound
  task on the Celery Task Queue- allowing you to scale your outbound messaging
  to your liking.


Running The Unit Tests
----------------------

.. code-block:: text

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

