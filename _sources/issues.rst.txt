Known ISSUES
============

Matplotlib 3 in Mac OS X
------------------------

In the case of using matplotlib 3 under Mac OS X (installations starting
in 2019), in order to avoid a potential error associated to the use of
the ``libc++abi.dylib`` library by the TkAgg backend, we recommend you to
add the following line to the ``$HOME/.matplotlib/matplotlibrc`` file (you
should create the file if this does not exist):

.. code-block:: console

   (megara) $ more $HOME/.matplotlib/matplotlibrc

.. code-block:: console
   :class: my-special-block no-copybutton

   backend: TkAgg

Note that TkAgg is the default backend in Mac OS X. If you want to use
alternative ones they also need to be installed, or course.

Compiling in Mac OS X 10.10 or later
------------------------------------

Should the user be insterested in compiling part of the software on
their own, we note that in the case of the distribution of Mac OS X
10.10 or later they should include the following environment variable in
the ``$HOME/.bashrc`` shell configuration file:

.. code-block:: console

    (megara) $ more $HOME/.bashrc

.. code-block:: console
   :class: my-special-block no-copybutton

    export MACOSX_DEPLOYMENT_TARGET=10.9

Bash shell
----------

Bash shell is the default shell for using the MEGARA DRP and the
**megara-tools**. Please, be aware that starting on Mac OS X 10.15
“Catalina” the default shell is zsh. Tests on zsh have not yet been
performed to ensure its compatibility MEGARA DRP and **megara-tools**.
