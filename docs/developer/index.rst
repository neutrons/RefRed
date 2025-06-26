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


Contents:
---------

.. toctree::
   :maxdepth: 1

   pycharm
   testing
