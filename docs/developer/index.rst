.. _contents:

=======================
Developer Documentation
=======================

These pages contain the developer documentation. They are aimed at those who are modifying the
source code of the project.

Quick tasks, such as building the documentation can be carried out with `pixi` tasks at the top of the repository:

.. code-block:: bash

   ❯ pixi task list                                                                                                                                                                                                                (RefRed)
   Tasks that can run on this machine:
   -----------------------------------
   audit-deps, build-docs, clean, clean-all, clean-conda, clean-docs, conda-build, conda-build-command, conda-publish, reset-version, sync-version, test, test-docs
   Task                 Description
   audit-deps           Audit the package dependencies for vulnerabilities
   build-docs           Build documentation
   clean                Clean up various caches and build artifacts
   clean-all            Clean all artifacts
   clean-conda          Clean the local .conda build artifacts
   clean-docs           Clean up documentation build artifacts
   conda-build          Build the conda package
   conda-build-command  Wrapper for building the conda package - used by `conda-build`
   conda-publish        Publish the .conda package to anaconda.org
   reset-version        Reset the package version to 0.0.0
   sync-version         Sync pyproject.toml version with Git version
   test                 Run the test suite


Building conda packages
-----------------------

To build the conda package, use the `pixi` task:

.. code-block:: bash

   ❯ pixi run conda-build
   Building conda package...
   Packaging complete: refred-*.conda created in the current directory.


The GitHub actions workflow will automatically build and test the conda package,
but to manually install and test the conda package, use `micromamba`, `mamba`, or `conda`:

.. code-block:: bash
   mdkir -p /tmp/local-channel/linux-64
   cp refred-*.conda /tmp/local-channel/linux-64
   micromamba create -n refred --yes python=3.10  # same python version as in the pixi environment
   micromamba activate refred
   micromamba install --yes -c conda-forge conda-build conda-index
   python -m conda_index /tmp/local-channel
   # in addition to local-channel, use below the channels listed in file pyproject.toml
   micromamba install --yes -c /tmp/local-channel -c conda-forge -c neutrons/label/rc -c mantid-ornl refred
   # test the package and its most important dependencies are available
   python -c "import refred; import lr_reduction; import mantid; import qtpy"


Contents:
---------

.. toctree::
   :maxdepth: 1

   pycharm
   testing
