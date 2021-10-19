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
All other contributions should be done through
`Merge Requests <https://docs.gitlab.com/ee/user/project/merge_requests/getting_started.html>`_.

Creating a Local Environment for Development
--------------------------------------------

[To be completed]

* This project is configured to use the pre-commit framework. Please `configure the git hook <https://pre-commit.com/#3-install-the-git-hook-scripts>`_ by running ``pre-commit install``.

Coding
------

A few markers:

* descriptive variable names are preferred over cryptic short-name variables
* lower case variable names, CamelCase for class names
* `Numpy style <https://numpydoc.readthedocs.io/en/latest/format.html>`_ for docstrings
* (recommended) `type hints <https://docs.python.org/3/library/typing.html>`_ for function signatures and return values

For style details, consult the `PEP8 standard <https://www.python.org/dev/peps/pep-0008/>`_

It is highly recommended that you use the automatic code formatter by running once the command on your local repo:

.. code-block:: bash

    pre-commit install

Then `pre-commit` will automatically format your code every time you commit any files (`git commit ...`). Notice
that `pre-commit` may change some of the files to be committed. When this happens, you'll have to OK these changes
by re-staging the files, then committing again. This gives you a chance to review the changes brought about by
`pre-commit`.


Contacting the Team
-------------------
The best mechanism for contacting the team is to "open a ticket".
Otherwise, please email us at, Peter Peterson, at petersonpf &lt;at> ornl DOT gov.
