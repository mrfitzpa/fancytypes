.. _installation_instructions_sec:

Instructions for installing and uninstalling ``fancytypes``
===========================================================



Installing ``fancytypes``
-------------------------

For all installation scenarios, first open up the appropriate command line
interface. On Unix-based systems, you could open e.g. a terminal. On Windows
systems you could open e.g. an Anaconda Prompt as an administrator.



Installing ``fancytypes`` using ``pip``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before installing ``fancytypes``, make sure that you have activated the
(virtual) environment in which you intend to install said package. After which,
simply run the following command::

  pip install fancytypes

The above command will install the latest stable version of ``fancytypes``.

To install the latest development version from the main branch of the
`fancytypes GitHub repository <https://github.com/mrfitzpa/fancytypes>`_, one
must first clone the repository by running the following command::

  git clone https://github.com/mrfitzpa/fancytypes.git

Next, change into the root of the cloned repository, and then run the following
command::

  pip install .

Note that you must include the period as well. The above command executes a
standard installation of ``fancytypes``.

Optionally, for additional features in ``fancytypes``, one can install
additional dependencies upon installing ``fancytypes``. To install a subset of
additional dependencies (along with the standard installation), run the
following command from the root of the repository::

  pip install .[<selector>]

where ``<selector>`` can be one of the following:

* ``tests``: to install the dependencies necessary for running unit tests;
* ``examples``: to install the dependencies necessary for executing files stored
  in ``<root>/examples``, where ``<root>`` is the root of the repository;
* ``docs``: to install the dependencies necessary for documentation generation;
* ``all``: to install all of the above optional dependencies.

Alternatively, one can run::

  pip install fancytypes[<selector>]

elsewhere in order to install the latest stable version of ``fancytypes``, along
with the subset of additional dependencies specified by ``<selector>``.



Installing ``fancytypes`` using ``conda``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before proceeding, make sure that you have activated the (virtual) ``conda``
environment in which you intend to install said package.

To install ``fancytypes`` using the ``conda`` package manager, run the following
command::

  conda install -c conda-forge fancytypes

The above command will install the latest stable version of ``fancytypes``.



Uninstalling ``fancytypes``
---------------------------

If ``fancytypes`` was installed using ``pip``, then to uninstall, run the
following command::

  pip uninstall fancytypes

If ``fancytypes`` was installed using ``conda``, then to uninstall, run the
following command::

  conda remove fancytypes
