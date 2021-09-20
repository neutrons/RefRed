#- python setup.py install
# Replace dep1 dep2 ... with your dependencies
conda create -q -n test-environment python=$PYTHON_VERSION numpy pyqt=4;
source activate test-environment
conda config --add channels conda-forge
#- conda config --add channels mantid
#- conda install --yes -c mantid/label/nightly mantid-framework
pip install --upgrade codecov
pip install flake8
pip install numpy
flake8 --exit-zero --statistics --config build_tools/flake8.cfg RefRed
cd test;coverage run peak_finder_derivation_test.py