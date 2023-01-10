|Build Status|
|Codecov|
|DOI|
|CII Best Practices|

.. |Build Status| image:: https://github.com/neutrons/RefRed/actions/workflows/test-and-deploy.yml/badge.svg?branch=next
   :target: https://github.com/neutrons/RefRed/actions?query=branch:next

.. |Codecov| image:: https://codecov.io/gh/neutrons/RefRed/branch/next/graph/badge.svg?token=U9MNp8N9Lc
   :target: https://codecov.io/gh/neutrons/RefRed

.. |DOI| image:: https://zenodo.org/badge/39512610.svg
   :target: https://zenodo.org/badge/latestdoi/39512610

.. |CII Best Practices| image:: https://bestpractices.coreinfrastructure.org/projects/5312/badge
   :target: https://bestpractices.coreinfrastructure.org/projects/5312

------
RefRed
------

Data Reduction Software for the Liquids Reflectometer at the Spallation Neutron Source at Oak Ridge National Laboratory (ORNL)

------------
Contributing
------------

Contributing is done by adding to the source code base, as well writing tests and documentation (see
`Merge Requests <https://docs.gitlab.com/ee/user/project/merge_requests/getting_started.html>`_).
See `CONTRIBUTING.rst <CONTRIBUTING.rst>`_ for more information.

----------
Deployment
----------

- The state of branch `next` is deployed on every push-commit with the CI of [conda-legacy-deploy](https://code.ornl.gov/sns-hfir-scse/deployments/conda-legacy-deploy), by automatically launching a pipeline of branch `main` with environment variables `PLAY=update` and `CONDA_ENV=refred-dev`
