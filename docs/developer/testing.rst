.. _testing:

=======
Testing
=======

Running Manual tests in a Pull Request
======================================
If you are the reviewer of a Pull Request and you're supposed to run a manual test, you need to set up
the environment first:

Before running the manual tests, create conda environment `refred` and install the source in editable mode

.. code-block:: bash

   make conda-env



After that, start the GUI from the root path of the repository:

.. code-block:: bash

   > conda activate refred  # if not active
   (refred)> PYTHONPATH=$(pwd):$PYTHONPATH ./scripts/start_refred.py

and proceed with the test.
