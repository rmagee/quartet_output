Parsing and Evaluation
======================

The following modules and classes are responsible for the parsing and subsequent
filtering and evaluation of inbound EPCIS data in order to determine if an
outbound message should be sent.

Parsing
-------
The parsing classes in this package are inherited from the
standard quartet_epcis parsing classes; however, these classes
implement the output parsing logic by looping in the evaluation
functionality included in the `evaluation` module.

.. automodule:: quartet_output.parsing
    :show-inheritance:
    :inherited-members:
    :members:

Evaluation
----------
The classes defined in the evaluation module are responsible for
inspecting inbound EPCIS data and determining, based on the state
of a given output criteria model, whether or not an outbound message
should be generated and queued for transport.

.. automodule:: quartet_output.evaluation
    :show-inheritance:
    :inherited-members:
    :members:
