#- python setup.py install
python -m flake8 --exit-zero --statistics --config build_tools/flake8.cfg RefRed
cd test;python -m coverage run peak_finder_derivation_test.py