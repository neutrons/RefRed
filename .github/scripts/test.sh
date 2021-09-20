#- python setup.py install
conda activate test-environment
conda flake8 --exit-zero --statistics --config build_tools/flake8.cfg RefRed
cd test;conda coverage run peak_finder_derivation_test.py