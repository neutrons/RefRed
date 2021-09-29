flake8 --exit-zero --statistics RefRed
python -m pytest --cov=RefRed --cov-report=xml --cov-report=term test
