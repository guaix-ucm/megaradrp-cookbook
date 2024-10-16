.. _DRP_installation:

DRP installation
================

The MEGARA pipeline is a Python package, for Python 3.9 or greater.

The easiest method of installing megaradrp is using ``pip`` inside a virtual
environment.
You can install official relares or the development version.
All the commands in the following sections, starting with ``$`` 
are to be run under **bash shell**. 

Install with pip
----------------

A virtual environment creates isolated Python installations, with 
(potentially) different package versions.
We will use the venv package (a module in the standard library) 
here, although the `virtualenv package
<https://virtualenv.pypa.io/en/latest/>`_ can also be used.

The steps to run MEGARA DRP in a virtual environment are:

Create a virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A virtual environment will have a *name* and a *path*.
In order to create a virtual environment called e.g. megara using venv:

.. code-block:: console

    $ python3 -m venv megara /path/to/

With virtualenv:

.. code-block:: console

    $ virtualenv-3 megara /path/to/

The directory ``/path/to`` represents the location of the environment.

It can be any valid directory path.
If the path name is not specified, it will be created in the 
working directory (notice that
virtual environments shouldn't be moved after creation).

Activate the environment
~~~~~~~~~~~~~~~~~~~~~~~~

After creating the environment, the directory ``/path/to/megara``
contains a Python tree. One of the directories is
``/path/to/megara/bin``, which contains a script called ``activate``. To
activate the environment, we source (a bash shell command) this script
file:

.. code-block:: console

    $ source /path/to/megara/bin/activate

which yields a different system prompt to the user:

.. code-block:: console

    (megara) $

Now, the name of the environment appears before the standard prompt. We
can use the environment only on those consoles / terminals where we have
previously activated it.

Install megaradrp with pip
~~~~~~~~~~~~~~~~~~~~~~~~~~

After the activation, we can install megaradrp with pip. This is the
standard Python tool for package management. It will download the
package and its dependencies, unpack everything and compile when needed.

What follows is a sample of the output:

.. code-block:: console

    (megara) pip install megaradrp
    Collecting megaradrp
    Collecting scikit-image (from megaradrp)
    Downloading https://files.pythonhosted.org/packages/11/c7/ee75c79dcce057a3475763d611ec044737a708eaf5cc53426b0117795ddb/scikit_image-0.14.0-cp35-cp35mu-manylinux1_x86_64.whl (25.4MB)
    Collecting scipy (from megaradrp)
    (...)
    Building wheels for collected packages: toolz, scandir
    Running setup.py bdist_wheel for toolz ... done
    Running setup.py bdist_wheel for scandir ... done
    Successfully built toolz scandir
    Installing collected packages: decorator, networkx, cloudpickle, numpy,
    toolz, dask, six, PyWavelets, python-dateutil, subprocess32, cycler,
    backports.functools-lru-cache, pytz, pyparsing, kiwisolver, matplotlib,
    scipy, pillow, scikit-image, enum34, atomicwrites, more-itertools,
    pluggy, attrs, scandir, pathlib2, py, funcsigs, pytest, astropy, PyYaml,
    numina, megaradrp

Test the installation
~~~~~~~~~~~~~~~~~~~~~

Now we can test the installation by running the numina command:

.. code-block:: console
    
    (megara) $ numina show-instruments
    INFO: Numina simple recipe runner version 0.34
    Instrument: MEGARA
      version is '0.16'
       has profile 'Configuration at LICA' uuid=9a86b2b2-3f7d-48ec-8f4f-3780ec967c90
       has profile 'Configuration at GTC' uuid=ca3558e3-e50d-4bbc-86bd-da50a0998a48
       has profile 'Test component' uuid=4fd05b24-2ed9-457b-b563-a3c618bb1d4c
       has profile 'Configuration for the Simulator' uuid=66f2283e-3049-4d4b-8ef1-14d62fcb611d
       has datamodel 'megaradrp.datamodel.MegaraDataModel'
       has pipeline 'default', version 1

The particular output of the command may change, but ``Instrument: MEGARA`` text
should always appear.

Update within the environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to update the MEGARA DRP to the latest stable release,  the user
should execute:

.. code-block:: console
    
    (megara) $ pip install -U megaradrp

Deactivate the environment
~~~~~~~~~~~~~~~~~~~~~~~~~~

To exit the environment is enough to exit the terminal or run the
command deactivate.


.. code-block:: console

    (megara) $ deactivate
    $

Install in conda
----------------

`Conda <https://conda.io/docs/>`_ was created with a target similar 
to virtualenv, but know has
extended its functionallity to package management for different
languages.

You can install `miniconda <https://docs.anaconda.com/miniconda/>`_ or
`anaconda <https://www.anaconda.com/>`_. The difference is that
miniconda provides a light-weight environment and anaconda comes with
lots of Python packages.

If you have updated the ``$PATH`` variable during install, you can call
conda commands directly in the shell, like this:

.. code-block:: console

    $ conda info

If not, you will need to add the path to the command (an example path
could be ``miniconda3/bin``), like:

.. code-block:: console

    $ /path/to/conda/bin/conda info

If that is the case, you should add that path every time you run a conda
command hereafter. Alternatively, you can initialize conda for your own
shell by doing:

.. code-block:: console
    
    $ conda init bash

This works as it is if you are using a login-shell (terminal), but if
you are using an xterm, you might also need to do:

.. code-block:: console
    
    $ cp ~/.bash_profile ~/.bashrc 

(do a backup copy of ``~/.bashrc`` if you have one already),

and open a new terminal/xterm. Below, we will write the commands without the
full path, for simplicity.  If you are using conda version 4.4+ your terminal
will open in the conda *(base)* environment. If you want to avoid that
permanently just do: ``conda config --set auto_activate_base false``.


Once conda is installed according to the
instructions above, the steps to run MEGARA DRP under conda would be the
following:

Create a conda environment
~~~~~~~~~~~~~~~~~~~~~~~~~~

We first recommend that you update your conda installation to its latest
by doing:

.. code-block:: console
    
    (base) $ conda update conda

With conda, environments are created in a centralised manner (under
directory ``./envs`` in your conda tree), we do not pass the path to the
environment.

.. code-block:: console
    
    (base) $ conda create --name megara python=3

One could remove this environment (and all its content), if needed, by
simply doing:

.. code-block:: console
    
    (base) $ conda remove --name megara --all

Install megaradrp with conda
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Packages can be installed before activating the environment. We provide conda
packages for megaradrp in the  `conda-forge channel
<https://conda-forge.org/>`_

.. code-block:: console

    (base) $ conda install --name megara -c conda-forge megaradrp
    Fetching package metadata .............
    Solving package specifications: .
    Package plan for installation in environment /home/xxx/devel/miniconda3/envs/megara:
    The following NEW packages will be INSTALLED:
    astropy: 2.0.8-py35_0 conda-forge
    atomicwrites: 1.1.5-py35_0 conda-forge
    attrs: 18.1.0-py_1 conda-forge
    ....
    zlib: 1.2.11-h470a237_3 conda-forge
    Proceed ([y]/n)? y


Activate the environment
~~~~~~~~~~~~~~~~~~~~~~~~

The functionality is similar to virtualenv:

.. code-block:: console

    (base) $ conda activate megara
    (megara) $

Again, after activating the environment, the name of the environment
appears before the standard prompt. We can use the environment only on
those consoles / terminals where we have previously activated it.

Test the installation
~~~~~~~~~~~~~~~~~~~~~

Now we can test the installation by running the numina command:

.. code-block:: console

    (megara) $ numina show-instruments
    INFO: Numina simple recipe runner version 0.34
    Instrument: MEGARA
      version is '0.16'
       has profile 'Configuration at LICA' uuid=9a86b2b2-3f7d-48ec-8f4f-3780ec967c90
       has profile 'Configuration at GTC' uuid=ca3558e3-e50d-4bbc-86bd-da50a0998a48
       has profile 'Test component' uuid=4fd05b24-2ed9-457b-b563-a3c618bb1d4c
       has profile 'Configuration for the Simulator' uuid=66f2283e-3049-4d4b-8ef1-14d62fcb611d
       has datamodel 'megaradrp.datamodel.MegaraDataModel'
       has pipeline 'default', version 1


Update within the environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to update the MEGARA DRP within the conda environment the user
should execute:

.. code-block:: console
    
    (megara) $ conda update megaradrp

Deactivate the environment
~~~~~~~~~~~~~~~~~~~~~~~~~~

To exit the environment is enough to exit the terminal or run the
command source deactivate

.. code-block:: console

    (megara) $ conda deactivate
    (base) $

Update outside the environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once outside the conda environment one can also update the MEGARA DRP
installation by doing:

.. code-block:: console
    
    (base) $ conda update megaradrp -n megara

If you want to deactivate the conda *(base)* environment entirely you
can run again:

.. code-block:: console
    
    (base) $ conda deactivate
    $

Development version
-------------------

For those of you interested in installing the development version,
please consult the instructions at the readthedocs.org webpage at
https://megaradrp.readthedocs.io/en/latest/installation.html. The use of
the development version is recommended to have access to the latest DRP
improvements.


