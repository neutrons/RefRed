#- python setup.py install
activate test-environment
flake8 --exit-zero --statistics --config build_tools/flake8.cfg RefRed
cd test;coverage run peak_finder_derivation_test.py