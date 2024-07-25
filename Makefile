# bash sell to correctly interpret the double brackets in the conditions below
SHELL=/bin/bash
# https://www.gnu.org/software/make/manual/html_node/One-Shell.html
# Required to prevent having to use "conda init"

# command to run docker compose. change this to be what you have installed
# this can be overriden on the command line
# DOCKER_COMPOSE="docker compose" make startdev
DOCKER_COMPOSE ?= docker-compose
# name for docker image to run the CI in
DOCKER_CI_TAG ?= web_reflectivity_test

# all the lines in a recipe are passed to a single invocation of the shell.
.ONESHELL:

# list of all phony targets, alphabetically sorted
.PHONY: help conda docs test

help:
    # this nifty perl one-liner collects all commnents headed by the double "#" symbols next to each target and recycles them as comments
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

# Note that the extra activate is needed to ensure that the activate floats env to the front of PATH
CONDA_ACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate
conda-env:  ## creates conda environment `refred` and installs package `RefRed` in editable mode
	conda env create --solver=libmamba --file ./environment.yml
	$(CONDA_ACTIVATE) refred
	pip install -e .

docs:  ## create HTML docs under `docs/_build/html/`. Requires activation of the `refred` conda environment
	# this will fail on a warning
	@cd docs&& make html SPHINXOPTS="-W --keep-going -n" && echo -e "##########\n DOCS point your browser to file://$$(pwd)/_build/html/index.html\n##########"

test-all:  ## run all tests
	pytest ./test
