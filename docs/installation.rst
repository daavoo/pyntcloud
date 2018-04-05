.. _installation:

============
Installation
============

Minimum Requirements
====================

At the very least, you need a Python(3) installation (an isolated environment, i.e conda, is recommended) and the following requirements:

- numpy
- numba
- scipy
- pandas

You can install this requirements however you want to although we recommend to use minconda:

https://conda.io/miniconda.html

And running:

.. code-block:: bash
    
    conda env create -n pyntcloud python=3 numpy numba scipy pandas

    source activate pyntcloud 


Basic Installation
==================

Once you have this requirements installed, you can install pyntcloud using:

.. code-block:: bash

    pip install git+https://github.com/daavoo/pyntcloud


Installation for developers
===========================

Check :ref:`contributing`
