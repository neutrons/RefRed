.. _contents:

=======================
Developer Documentation
=======================

These pages contain the developer documentation. They are aimed at those who are modifying the
source code of the project.

Quick tasks, such as building the documentation can be carried out with the Makefile at the top of the repository:

.. code-block:: bash

   ❯ make help
   conda-env    creates conda environment `refred` and installs package `RefRed` in editable mode
   docs         create HTML docs under `docs/_build/html/`. Requires previous activation of the `refred` conda environment
   test-all     run all tests with pytest


Contents:
---------

.. toctree::
   :maxdepth: 1

   pycharm
   testing
