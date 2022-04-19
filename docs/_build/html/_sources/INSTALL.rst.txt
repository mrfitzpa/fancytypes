.. _installation_instructions_sec:

Installation instructions
=========================

Install fancytypes
------------------

First, open up the appropriate command line interface. On Unix-based systems,
you would open a terminal. On Windows systems you would open an Anaconda Prompt
as an administrator.

Next, assuming that you have downloaded/cloned the ``fancytypes`` git
repository, change into the root of said repository, and run the following
command::

  pip install .

Note that you must include the period as well. This will install ``fancytypes``
along with all of its dependencies, namely ``numpy``, ``czekitout``, and
``pytest``.

Update fancytypes
-----------------

If you, or someone else has made changes to this library, you can reinstall it
by issuing the following command::
  
    pip install .

Uninstall fancytypes
--------------------

To uninstall ``fancytypes``, all you need to type is::

  pip uninstall fancytypes

Exploring examples of using fancytypes
--------------------------------------

Examples of using ``fancytypes`` can be found in a set of notebooks in the
directory ``<root>/examples``, where ``<root>`` is the root of the
repository. In order to open the notebooks and run cells, one must install
``jupyter-notebook``. One can install ``jupyter-notebook`` by running the
following commands from the root of the repository::

  pip3 install --upgrade pip
  pip3 install -r requirements-examples.txt

Since the repository tracks the notebooks under their original basenames, we
recommend that you copy whatever original notebook of interest and rename it to
whatever other basename before executing any cells. This way you can explore any
notebook by executing and modifying cells without changing the originals, which
are being tracked by git.

Generating documention files
----------------------------

To generate documentation in html format from source files, you will also need
to install several other packages. This can be done by running the following
command from the root of the repository::

  pip install -r requirements-doc.txt

Next, assuming that you are in the root of the repository, that you have
installed all the prerequisite packages, and that ``fancytypes`` has been
installed, you can generate the ``fancytypes`` documentation html files by
issuing the following commands within your virtual environment::

  cd docs
  make html

This will generate a set of html files in ``./_build/html`` containing the
documentation of ``fancytypes``. You can then open any of the files using your
favorite web browser.

If ``fancytypes`` has been updated, the documentation has most likely changed as
well. To update the documentation simply run::

  make html

again to generate the new documentation.
