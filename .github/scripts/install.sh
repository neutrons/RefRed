# Useful for debugging any issues with conda
conda info -a

conda create -q -n test-environment python=$PYTHON_VERSION numpy pyqt=4;
source activate test-environment
pip install -r requirements.txt -r requirements_dev.txt