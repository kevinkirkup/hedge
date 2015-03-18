hedge - Financial Python module
===============

# Setup

## Install Python packages

There are a number of packages that we will be using in python. Most of them
are from SciPy but there are others that we will use. We will be using
VirtualEnv and pip to install our local development system. We will assume
that you already have iPython installed in the global site-packages and we
will not reinstall it here.

    $ virtualenv venv

Source our environment

    $ source venv/bin/activate

Install the list of packages:

    $ pip install numexpr cython pqzmq h5py tornado tables pandas ipdb numpy scipy matplotlib

Install python packages to bridge between iPython Notebook and R.

    $ pip install rpy2
