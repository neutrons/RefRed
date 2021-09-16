#- sudo apt-get update
# We do this conditionally because it saves us some downloading if the
# version is the same.
if [[ "$PYTHON_VERSION" == "2.7" ]]; then
  wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -O miniconda.sh;
else
  wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh;
fi
bash miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
hash -r
conda config --set always_yes yes --set changeps1 no
conda config --append channels conda-forge
conda update -q conda
# Useful for debugging any issues with conda
conda info -a
# Replace dep1 dep2 ... with your dependencies
conda create -q -n test-environment python=$PYTHON_VERSION numpy pyqt=4;
source activate test-environment
conda config --add channels conda-forge
#- conda config --add channels mantid
#- conda install --yes -c mantid/label/nightly mantid-framework
pip install --upgrade codecov
pip install flake8