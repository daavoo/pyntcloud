.. _basic-installation:

==================
Basic installation
==================

Requirements
============

At the very least, you need a Python(3) installation and the following requirements:

- ipython
- laspy
- matplotlib
- numpy
- numba
- scipy
- pandas
- python-lzf

You can install this requirements however you want to.

Once you have this requirements installed, you can install pyntcloud using:

.. code-block:: bash

    pip install git+https://github.com/daavoo/pyntcloud

Using conda
===========

We provide you a easier installation using conda.

First, install https://conda.io/miniconda.html.

Then, download the conda enviroment file at:

https://raw.githubusercontent.com/daavoo/pyntcloud/master/env.yml

You can manually save the content to a file or use:

.. code-block:: bash

    wget https://raw.githubusercontent.com/daavoo/pyntcloud/master/env.yml

After that, type in a terminal:

.. code-block:: bash
    
    conda env create -f env.yml

    source activate pyntcloud

    pip install git+https://github.com/daavoo/pyntcloud


Installation for developers
===========================

If you want to hack around pyntcloud, there are a few more requirements:

- autopep8
- flake8
- pytest

If you are using conda, create an enviroment using the following file instead of the env.yml:

https://raw.githubusercontent.com/daavoo/pyntcloud/master/dev_env.yml


Once you have the requirements installed, you can install pyntcloud in development mode as follows:

.. code-block:: bash

    git clone https://github.com/daavoo/pyntcloud.git
    
    cd pyntcloud

    # if conda
    source activate pyntcloud

    pip install -e .

From the root of the repo, you can run:

.. code-block:: bash

    # for auto-formating the code
    autopep8

    # for getting warnings about syntax and other kind of errors
    falke8

    # for running all the tests
    pytest -v
