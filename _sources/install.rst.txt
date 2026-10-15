.. _DRP_installation:

DRP installation
================

The MEGARA pipeline is a Python package, for Python 3.10 or greater.

The easiest method of installing **megaradrp** is using ``pip`` inside a
virtual environment. You can install official relares or the development
version. All the commands in the following sections, starting with ``$`` are
to be run under **bash shell**.

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
   :class: no-copybutton

   $ python3 -m venv /path/to/megara

With virtualenv:

.. code-block:: console
   :class: no-copybutton

   $ virtualenv /path/to/megara

The directory ``/path/to/megara`` represents the location of the environment.

It can be any valid directory path.
If only a name is given (for example ``megara``), it will be created in the
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
   :class: no-copybutton

   $ source /path/to/megara/bin/activate

which yields a different system prompt to the user:

.. code-block:: console
   :class: no-copybutton

   (megara) $

Now, the name of the environment appears before the standard prompt. We
can use the environment only on those consoles / terminals where we have
previously activated it.

Install megaradrp with pip
~~~~~~~~~~~~~~~~~~~~~~~~~~

After the activation, we can install **megaradrp** with pip. This is the
standard Python tool for package management. It will download the
package and its dependencies, unpack everything and compile when needed.

What follows is a sample of the output:

.. code-block:: console

   (megara) $ pip install megaradrp

If you want to guarantee that **megaradrp** is completely reinstalled (even if
it is already installed), downloading it again, without using any cached wheel
or source distribution, you can use:

.. code-block:: console

   (megara) $ pip install --no-cache-dir --force-reinstall megaradrp

.. code-block:: console
   :class: my-special-block no-copybutton

   Collecting megaradrp
     Downloading megaradrp-0.22-py3-none-any.whl.metadata (3.2 kB)
   Collecting astropy>=6.1.7 (from megaradrp)
     Downloading astropy-8.0.1-cp311-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (11 kB)
   Collecting attrs (from megaradrp)
     Downloading attrs-26.1.0-py3-none-any.whl.metadata (8.8 kB)
   Collecting jsonschema (from megaradrp)
     Downloading jsonschema-4.26.0-py3-none-any.whl.metadata (7.6 kB)
   Collecting matplotlib (from megaradrp)
     Downloading matplotlib-3.11.2-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (80 kB)
   Collecting numina>=0.40.0 (from megaradrp)
     Downloading numina-0.40.0-cp314-cp314-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl.metadata (3.7 kB)
   ...
   ...
   Installing collected packages: slicerator, urllib3, uncertainties, typing-extensions, tqdm, toolz, six, rpds-py, PyYAML, pyparsing, pygments, pyavm, platformdirs, pillow, packaging, numpy, networkx, msgspec, mdurl, locket, kiwisolver, idna, google-crc32c, fsspec, fonttools, dill, cycler, cloudpickle, click, charset_normalizer, certifi, attrs, astropy-iers-data, asteval, tifffile, spherical-geometry, scipy, requests, referencing, python-dateutil, pyerfa, partd, numcodecs, markdown-it-py, lazy-loader, imageio, donfig, contourpy, zarr, scikit-image, rich, pooch, pims, matplotlib, lmfit, jsonschema-specifications, dask, astropy, rich-argparse, jsonschema, astroscrappy, astropy-healpix, teareduce, dask-image, reproject, ccdproc, numina, megaradrp
   Successfully installed PyYAML-6.0.3 asteval-1.0.10 astropy-8.0.1 astropy-healpix-2.0.1 astropy-iers-data-0.2026.10.12.1.3.27 astroscrappy-1.3.0 attrs-26.1.0 ccdproc-2.5.1 certifi-2026.7.22 charset_normalizer-3.5.2 click-8.5.0 cloudpickle-3.1.2 contourpy-1.4.0 cycler-0.12.1 dask-2026.8.0 dask-image-2026.5.0 dill-0.4.1 donfig-0.8.1.post1 fonttools-4.67.0 fsspec-2026.9.0 google-crc32c-1.9.0 idna-3.20 imageio-2.38.1 jsonschema-4.26.0 jsonschema-specifications-2025.9.1 kiwisolver-1.5.1 lazy-loader-0.6 lmfit-1.3.4 locket-1.0.0 markdown-it-py-4.2.0 matplotlib-3.11.2 mdurl-0.1.2 megaradrp-0.22 msgspec-0.22.0 networkx-3.7 numcodecs-0.17.0 numina-0.40.0 numpy-2.5.4 packaging-26.3 partd-1.4.2 pillow-12.3.0 pims-0.7 platformdirs-4.13.0 pooch-1.9.0 pyavm-0.9.9 pyerfa-2.0.1.5 pygments-2.21.0 pyparsing-3.3.3 python-dateutil-2.9.0.post0 referencing-0.37.0 reproject-0.21.0 requests-2.34.2 rich-15.0.0 rich-argparse-1.8.0 rpds-py-2026.9.1 scikit-image-0.26.0 scipy-1.18.1 six-1.17.0 slicerator-1.1.0 spherical-geometry-1.4.0 teareduce-0.7.9 tifffile-2026.9.20 toolz-1.2.0 tqdm-4.70.1 typing-extensions-4.16.0 uncertainties-3.2.3 urllib3-2.8.0 zarr-3.4.1

Test the installation
~~~~~~~~~~~~~~~~~~~~~

Now we can test the installation by running the numina command:

.. code-block:: console

   (megara) $ numina --version

.. code-block:: console
   :class: my-special-block no-copybutton

   numina 0.40.0

.. code-block:: console

   (megara) $ numina show-instruments

.. code-block:: console
   :class: my-special-block no-copybutton

   INFO: Numina simple recipe runner version 0.40.0
   Instrument: MEGARA
    version is '0.22'
    has profile 'Configuration at LICA' uuid=9a86b2b2-3f7d-48ec-8f4f-3780ec967c90
    has profile 'MEGARA@GTC after November 2025' uuid=9f3fecbf-376c-47ae-a188-313b7d829104
    has profile 'Configuration for the Simulator' uuid=66f2283e-3049-4d4b-8ef1-14d62fcb611d
    has profile 'MEGARA@GTC between 2017 and 2024' uuid=ca3558e3-e50d-4bbc-86bd-da50a0998a48
    has profile 'Test component' uuid=4fd05b24-2ed9-457b-b563-a3c618bb1d4c
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
   :class: no-copybutton

   (megara) $ deactivate
   $

Install in a conda environment
------------------------------

The packages of **megaradrp** and **numina** in the `conda-forge channel
<https://conda-forge.org/>`_ are no longer updated: they are older versions,
and some dependencies of numina are not in conda-forge. If you use `conda
<https://docs.conda.io/>`_ (for example with `miniforge
<https://github.com/conda-forge/miniforge>`_ or `miniconda
<https://docs.anaconda.com/miniconda/>`_), create the environment with conda
and install **megaradrp** in it with pip, from PyPI.

Create and activate a conda environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With conda, environments are created in a centralised manner (under
directory ``./envs`` in your conda tree), we do not pass the path to the
environment:

.. code-block:: console
   :class: no-copybutton

   (base) $ conda create --name megara python=3.12
   (base) $ conda activate megara
   (megara) $

Install megaradrp with pip
~~~~~~~~~~~~~~~~~~~~~~~~~~

Inside the conda environment, install **megaradrp** with pip, as in the
virtual environment:

.. code-block:: console

   (megara) $ pip install megaradrp

Avoid installing or updating afterwards with conda, in that environment, the
packages that pip has installed. The installation can be tested as described
above. To update the MEGARA DRP:

.. code-block:: console

   (megara) $ pip install -U megaradrp

To exit the environment, run ``conda deactivate``. The environment (and all
its content) can be removed, if needed, with:

.. code-block:: console
   :class: no-copybutton

   (base) $ conda remove --name megara --all

Development version
-------------------

For those of you interested in installing the development version,
please consult the instructions at the readthedocs.org webpage at
https://megaradrp.readthedocs.io/en/latest/installation.html. The use of
the development version is recommended to have access to the latest DRP
improvements.
