=====
Usage
=====

To use quartet_output in a project, add it to your `INSTALLED_APPS`:

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
