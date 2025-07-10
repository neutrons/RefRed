.. _testing:

=======
Testing
=======

Running Manual tests in a Pull Request
======================================

If you are the reviewer of a Pull Request and you're supposed to run a manual test,
you need to set up the environment first.

Create pixi environment and install the source in editable mode:

.. code-block:: bash

   $ pixi install

Then, start the GUI from the root path of the repository:

.. code-block:: bash

   $ pixi shell
   (refred) $ refred

   # or simply
   $ pixi run refred

and proceed with the test.
