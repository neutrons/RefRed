.. _testing:

=======
Testing
=======

Running Manual tests in a Pull Request
======================================
If you are the reviewer of a Pull Request and you're supposed to run a manual test, you need to set up
the environment first:

Before running the manual tests, create pixi environment `refred` and install the source in editable mode

.. code-block:: bash

   > pixi install

After that, start the GUI from the root path of the repository:

.. code-block:: bash

   > pixi shell

   (refred)
   > refred

or simply:

.. code-block:: bash

   > pixi run refred

and proceed with the test.
