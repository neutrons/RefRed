Guide to Contributing
=====================

Contributions to this project are welcome. All contributors agree to the following:
- You have permission and any required rights to submit your contribution.
- Your contribution is provided under the license of this project and may be redistributed as such.
- All contributions to this project are public.

All contributions must be
`"signed off" in the commit <https://git-scm.com/docs/git-commit#Documentation/git-commit.txt---signoff>`_
log and by doing so you agree to the above.

Getting access to the main project
----------------------------------

Direct commit access to the project is currently restricted to core developers.
All other contributions should be done through pull requests using the standard github mechanisms.

Creating a Local Environment for Development
--------------------------------------------

This project requires the `mantid <https://anaconda.org/mantid/mantid>`_ conda package, as well as python3.6+ and qt5.
These can be installed using the commands

.. code-block:: bash

   conda env create --file development.yml
   conda activate refred

Then the testsuite can be run via

.. code-block:: bash

   pytest --cov

or ``pytest path/to/testfile.py`` to run an individual test.

The main gui can be started via

.. code-block:: bash

   QT_API=pyqt5 python scripts/start_refred.py
   
The ``QT_API=pyqt5` tells qtpy to use the qt5 library.


Coding
------

A few markers:

* descriptive variable names are preferred over cryptic short-name variables
* lower case variable names, CamelCase for class names
* `Numpy style <https://numpydoc.readthedocs.io/en/latest/format.html>`_ for docstrings
* (recommended) `type hints <https://docs.python.org/3/library/typing.html>`_ for function signatures and return values

For style details, consult the `PEP8 standard <https://www.python.org/dev/peps/pep-0008/>`_.
This is enforced through using the `black formatter <https://black.readthedocs.io/en/stable/>`_.

It is highly recommended that you use the automatic code formatting and some static analysis enabling `pre-commit <https://pre-commit.com>`_.
Do so by running the following command once on your local clone:

.. code-block:: bash

    pre-commit install

Then `pre-commit` will automatically format your code every time you commit any files (`git commit ...`). Notice
that `pre-commit` may change some of the files to be committed. When this happens, you'll have to OK these changes
by re-staging the files, then committing again. This gives you a chance to review the changes brought about by
`pre-commit`.

Testing Policy
--------------

The RefRed project makes use of automated testing.
Before submitting a pull-request the developer is encouraged to run the full testsuite.
Pull requests should bear this in mind and note that requests that increase the test coverage are heavily preferred.
Requests will be automatically annotated with code coverage results to aid the contributor and development team.

While tests that use mock/fake data are preferred, it is understood that some may require actual data.
These can be found in ``test/data`` and should be used rather than putting additional data into the repository.
There are also some tests that are skipped on github either because of memory requirements/execution time, or that the input data is not being made available in the repository.
These can generally be found by looking for ``os.environ.get("GITHUB_ACTIONS", False)`` nearby them.

Contacting the Team
-------------------
The best mechanism for contacting the team is to "open a ticket".
Otherwise, please email us at, Peter Peterson, at petersonpf &lt;at> ornl DOT gov.
