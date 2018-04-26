.. _contributing:

============
Contributing
============

If you want to hack around with PyntCloud you should install the depencies specified in :ref:`installation`.

In addition to those, you need to install:

- flake8
- pytest

Then you can clone the repo and install it in editable mode:

.. code-block:: bash

    git clone https://github.com/daavoo/pyntcloud.git
    pip install -e pyntcloud

From the root of the repo, you can run:

.. code-block:: bash

    # for getting warnings about syntax and other kinds of errors
    flake8

    # for running all the tests
    pytest -v
