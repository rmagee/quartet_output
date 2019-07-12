Transport Mixins
================

Core Mixin Classes
------------------
The transport mixins provide the functionality for the `TransportStep`'s
outbound messaging capabilities.  Each mixin has the capabilities to understand
the different URN values that can be supplied in a given `models.EndPoint` and
to use the data in these URNs to send messages via HTTP, SMTP and SFTP.


.. automodule:: quartet_output.transport.http
    :show-inheritance:
    :inherited-members:
    :members:

.. automodule:: quartet_output.transport.mail
    :show-inheritance:
    :inherited-members:
    :members:

.. automodule:: quartet_output.transport.sftp
    :show-inheritance:
    :inherited-members:
    :members:
