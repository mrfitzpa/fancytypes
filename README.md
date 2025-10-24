# Fancy Types (FancyTypes)

[![Test library](https://github.com/mrfitzpa/fancytypes/actions/workflows/test_library.yml/badge.svg)](https://github.com/mrfitzpa/fancytypes/actions/workflows/test_library.yml)
[![Code Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/mrfitzpa/0ff284bfee8b5519e6f1bafa849007bb/raw/fancytypes_coverage_badge.json)](https://github.com/mrfitzpa/fancytypes/actions/workflows/measure_code_coverage.yml)
[![Documentation](https://img.shields.io/badge/docs-read-brightgreen)](https://mrfitzpa.github.io/fancytypes)
[![PyPi Version](https://img.shields.io/pypi/v/fancytypes.svg)](https://pypi.org/project/fancytypes)
[![Conda-Forge Version](https://img.shields.io/conda/vn/conda-forge/fancytypes.svg)](https://anaconda.org/conda-forge/fancytypes)
[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

``fancytypes`` is a simple Python library that contains a base class
representing an updatable parameter set that is equipped with methods to
facilitate parameter data serialization and validation.

Visit the `fancytypes` [website](https://mrfitzpa.github.io/fancytypes) for a
web version of the installation instructions, the reference guide, and the
examples archive.

The source code can be found in the [`fancytypes` GitHub
repository](https://github.com/mrfitzpa/fancytypes).



## Table of contents

- [Instructions for installing and uninstalling
  `fancytypes`](#instructions-for-installing-and-uninstalling-fancytypes)
  - [Installing `fancytypes`](#installing-fancytypes)
    - [Installing `fancytypes` using
      `pip`](#installing-fancytypes-using-pip)
    - [Installing `fancytypes` using
      `conda`](#installing-fancytypes-using-conda)
  - [Uninstalling `fancytypes`](#uninstalling-fancytypes)
- [Learning how to use `fancytypes`](#learning-how-to-use-fancytypes)



## Instructions for installing and uninstalling `fancytypes`



### Installing `fancytypes`

For all installation scenarios, first open up the appropriate command line
interface. On Unix-based systems, you could open e.g. a terminal. On Windows
systems you could open e.g. an Anaconda Prompt as an administrator.



#### Installing `fancytypes` using `pip`

Before installing `fancytypes`, make sure that you have activated the (virtual)
environment in which you intend to install said package. After which, simply run
the following command:

    pip install fancytypes

The above command will install the latest stable version of `fancytypes`.

To install the latest development version from the main branch of the [fancytypes
GitHub repository](https://github.com/mrfitzpa/fancytypes), one must first clone
the repository by running the following command:

    git clone https://github.com/mrfitzpa/fancytypes.git

Next, change into the root of the cloned repository, and then run the following
command:

    pip install .

Note that you must include the period as well. The above command executes a
standard installation of `fancytypes`.

Optionally, for additional features in `fancytypes`, one can install additional
dependencies upon installing `fancytypes`. To install a subset of additional
dependencies (along with the standard installation), run the following command
from the root of the repository:

    pip install .[<selector>]

where `<selector>` can be one of the following:

* `tests`: to install the dependencies necessary for running unit tests;
* `examples`: to install the dependencies necessary for executing files stored
  in `<root>/examples`, where `<root>` is the root of the repository;
* `docs`: to install the dependencies necessary for documentation generation;
* `all`: to install all of the above optional dependencies.

Alternatively, one can run:

    pip install fancytypes[<selector>]

elsewhere in order to install the latest stable version of `fancytypes`, along
with the subset of additional dependencies specified by `<selector>`.



#### Installing `fancytypes` using `conda`

To install `fancytypes` using the `conda` package manager, run the following
command:

    conda install -c conda-forge fancytypes

The above command will install the latest stable version of `fancytypes`.



### Uninstalling `fancytypes`

If `fancytypes` was installed using `pip`, then to uninstall, run the following
command:

    pip uninstall fancytypes

If `fancytypes` was installed using `conda`, then to uninstall, run the following
command:

    conda remove fancytypes



## Learning how to use `fancytypes`

For those new to the `fancytypes` library, it is recommended that they take a
look at the [Examples](https://mrfitzpa.github.io/fancytypes/examples.html) page,
which contain code examples that show how one can use the `fancytypes`
library. While going through the examples, readers can consult the [fancytypes
reference
guide](https://mrfitzpa.github.io/fancytypes/_autosummary/fancytypes.html) to
understand what each line of code is doing.