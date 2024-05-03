.. _testing:

=======
Testing
=======

Running Manual tests in a Pull Request
======================================
If you are the reviewer of a Pull Request and you're supposed to run a manual test, you need to set up
the environment first:

Before running the manual tests, install the conda environment and install the source in editable mode

.. code-block:: bash

   conda env create --solver libmamba --name refred-dev --file ./environment.yml
   conda activate refred-dev
   (refred-dev)> pip install -e .

After that, start the GUI from the root path of the repository:

.. code-block:: bash

   (refred-dev)> PYTHONPATH=$(pwd):$PYTHONPATH ./scripts/start_refred.py

and proceed with the test.
