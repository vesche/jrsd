jrsd (Jackson's Rogue System Detection)
=======================================

jrsd is a network device monitoring and alerting utility designed to run on a RHEL/CentOS host. It's built for an extremely specific use case of providing rogue system detection on a small, static network. This is accomplished by providing a complete whitelist of MAC addresses that will be used on the network, and periodically ARP scanning to ensure all network devices are within the whitelist.

Installation
------------

jrsd is distributed on `PyPI <https://pypi.org>`_ as a universal
wheel and is available on Linux/macOS and Windows and supports
Python 2.7/3.5+ and PyPy.

.. code-block:: bash

    $ python setup.py install

License
-------

jrsd is Unlicensed, do what you want with it. (http://unlicense.org)
