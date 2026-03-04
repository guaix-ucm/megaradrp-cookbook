.. _DRP_installation:

DRP installation
================

The MEGARA pipeline is a Python package, for Python 3.9 or greater.

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

   $ python3 -m venv megara /path/to/

With virtualenv:

.. code-block:: console
   :class: no-copybutton

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
it is already installed), downloading it again, whithout using any cached wheel
or source distribution, you can use:

.. code-block:: console

   (megara) $ pip install --no-cache-dir --force-reinstall megaradrp

.. code-block:: console
   :class: my-special-block no-copybutton

   Collecting megaradrp
     Downloading megaradrp-0.21-py2.py3-none-any.whl.metadata (3.2 kB)
   Collecting astropy>=6.1.7 (from megaradrp)
     Downloading astropy-7.2.0-cp311-abi3-macosx_11_0_arm64.whl.metadata (10 kB)
   Collecting attrs (from megaradrp)
     Downloading attrs-25.4.0-py3-none-any.whl.metadata (10 kB)
   Collecting jsonschema (from megaradrp)
     Downloading jsonschema-4.26.0-py3-none-any.whl.metadata (7.6 kB)
   Collecting matplotlib (from megaradrp)
     Downloading matplotlib-3.10.8-cp313-cp313-macosx_11_0_arm64.whl.metadata (52 kB)
   Collecting numpy (from megaradrp)
     Downloading numpy-2.4.2-cp313-cp313-macosx_14_0_arm64.whl.metadata (6.6 kB)
   Collecting numina>=0.37.0 (from megaradrp)
     Downloading numina-0.37.0.tar.gz (500 kB)
     Installing build dependencies ... done
     Getting requirements to build wheel ... done
     Preparing metadata (pyproject.toml) ... done
   ...
   ...
   Installing collected packages: slicerator, urllib3, uncertainties, typing-extensions, tqdm, toolz, six, rpds-py, PyYAML, pyparsing, pygments, pyavm, pyarrow, platformdirs, pillow, packaging, numpy, networkx, mdurl, locket, kiwisolver, importlib_resources, idna, google-crc32c, fsspec, fonttools, dill, cycler, cloudpickle, click, charset_normalizer, certifi, backports.entry_points_selectable, attrs, astropy-iers-data, asteval, tifffile, scipy, requests, referencing, python-dateutil, pyerfa, partd, numcodecs, markdown-it-py, lazy-loader, imageio, donfig, contourpy, zarr, scikit-image, rich, pooch, pims, pandas, matplotlib, lmfit, jsonschema-specifications, dask, astropy, spherical-geometry, rich-argparse, jsonschema, astroscrappy, astropy-healpix, teareduce, dask-image, reproject, ccdproc, numina, megaradrp
   Successfully installed PyYAML-6.0.3 asteval-1.0.8 astropy-7.2.0 astropy-healpix-1.1.3 astropy-iers-data-0.2026.3.2.0.47.4 astroscrappy-1.3.0 attrs-25.4.0 backports.entry_points_selectable-1.3.0 ccdproc-2.5.1 certifi-2026.2.25 charset_normalizer-3.4.4 click-8.3.1 cloudpickle-3.1.2 contourpy-1.3.3 cycler-0.12.1 dask-2026.1.2 dask-image-2025.11.0 dill-0.4.1 donfig-0.8.1.post1 fonttools-4.61.1 fsspec-2026.2.0 google-crc32c-1.8.0 idna-3.11 imageio-2.37.2 importlib_resources-6.5.2 jsonschema-4.26.0 jsonschema-specifications-2025.9.1 kiwisolver-1.4.9 lazy-loader-0.4 lmfit-1.3.4 locket-1.0.0 markdown-it-py-4.0.0 matplotlib-3.10.8 mdurl-0.1.2 megaradrp-0.21 networkx-3.6.1 numcodecs-0.16.5 numina-0.37.0 numpy-2.4.2 packaging-26.0 pandas-3.0.1 partd-1.4.2 pillow-12.1.1 pims-0.7 platformdirs-4.9.2 pooch-1.9.0 pyarrow-23.0.1 pyavm-0.9.8 pyerfa-2.0.1.5 pygments-2.19.2 pyparsing-3.3.2 python-dateutil-2.9.0.post0 referencing-0.37.0 reproject-0.19.0 requests-2.32.5 rich-14.3.3 rich-argparse-1.7.2 rpds-py-0.30.0 scikit-image-0.26.0 scipy-1.17.1 six-1.17.0 slicerator-1.1.0 spherical-geometry-1.3.5 teareduce-0.7.4 tifffile-2026.3.3 toolz-1.1.0 tqdm-4.67.3 typing-extensions-4.15.0 uncertainties-3.2.3 urllib3-2.6.3 zarr-3.1.5
   
Test the installation
~~~~~~~~~~~~~~~~~~~~~

Now we can test the installation by running the numina command:

.. code-block:: console
    
   (megara) $ numina

.. code-block:: console
   :class: my-special-block no-copybutton

   INFO: Numina simple recipe runner version 0.37.0

.. code-block:: console
    
   (megara) $ numina show-instruments

.. code-block:: console
   :class: my-special-block no-copybutton

   INFO: Numina simple recipe runner version 0.37.0
   Instrument: MEGARA
    version is '0.21'
    has profile 'MEGARA@GTC after November 2025' uuid=9f3fecbf-376c-47ae-a188-313b7d829104
    has profile 'Test component' uuid=4fd05b24-2ed9-457b-b563-a3c618bb1d4c
    has profile 'Configuration at LICA' uuid=9a86b2b2-3f7d-48ec-8f4f-3780ec967c90
    has profile 'Configuration for the Simulator' uuid=66f2283e-3049-4d4b-8ef1-14d62fcb611d
    has profile 'MEGARA@GTC between 2017 and 2024' uuid=ca3558e3-e50d-4bbc-86bd-da50a0998a48
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

Install in conda (outdated)
---------------------------

.. warning::

   We inform you that the **megaradrp** package is no longer distributed via
   conda. We have discontinued the conda packaging process, and future updates
   will not be made available through conda channels. From now on,
   **megaradrp** is maintained and distributed exclusively through PyPI.

   Please note that the instructions provided below are now obsolete and are
   preserved solely for historical reference. They describe legacy installation
   procedures that are no longer maintained or supported. For current
   installation and usage, please refer exclusively to the PyPI‑based workflow
   described above.

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
   :class: no-copybutton

   $ conda info

If not, you will need to add the path to the command (an example path
could be ``miniconda3/bin``), like:

.. code-block:: console
   :class: no-copybutton

   $ /path/to/conda/bin/conda info

If that is the case, you should add that path every time you run a conda
command hereafter. Alternatively, you can initialize conda for your own
shell by doing:

.. code-block:: console
   :class: no-copybutton
    
   $ conda init bash

This works as it is if you are using a login-shell (terminal), but if
you are using an xterm, you might also need to do:

.. code-block:: console
   :class: no-copybutton
    
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
   :class: no-copybutton
    
   (base) $ conda update conda

With conda, environments are created in a centralised manner (under
directory ``./envs`` in your conda tree), we do not pass the path to the
environment.

.. code-block:: console
   :class: no-copybutton
    
   (base) $ conda create --name megara python=3

One could remove this environment (and all its content), if needed, by
simply doing:

.. code-block:: console
   :class: no-copybutton
    
   (base) $ conda remove --name megara --all

Install megaradrp with conda
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Packages can be installed before activating the environment. We provide conda
packages for **megaradrp** in the  `conda-forge channel
<https://conda-forge.org/>`_

.. code-block:: console
   :class: no-copybutton

   (base) $ conda install --name megara -c conda-forge megaradrp

.. code-block:: console
   :class: my-special-block no-copybutton

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
   :class: no-copybutton

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

.. code-block:: console
   :class: my-special-block no-copybutton

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
   :class: no-copybutton

   (megara) $ conda deactivate
   (base) $

Update outside the environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once outside the conda environment one can also update the MEGARA DRP
installation by doing:

.. code-block:: console
   :class: no-copybutton
    
   (base) $ conda update megaradrp -n megara

If you want to deactivate the conda *(base)* environment entirely you
can run again:

.. code-block:: console
   :class: no-copybutton
    
   (base) $ conda deactivate
   $

Development version
-------------------

For those of you interested in installing the development version,
please consult the instructions at the readthedocs.org webpage at
https://megaradrp.readthedocs.io/en/latest/installation.html. The use of
the development version is recommended to have access to the latest DRP
improvements.


