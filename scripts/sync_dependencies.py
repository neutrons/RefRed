# standard imports
import logging
import os
import re
import sys

script_dir: str = os.path.dirname(os.path.realpath(__file__))
repo_dir: str = os.path.dirname(script_dir)


def check_dependencies_synced():
    r"""Check that the dependencies of environment.yml and requirements.txt are in sync"""

    conda_env = open(os.path.join(repo_dir, "environment.yml"), "r").read()
    reqs_env = open(os.path.join(repo_dir, "requirements.txt"), "r").read()

    # check for LiquidsReflectometer versions
    lr_conda = re.search(r"LiquidsReflectometer\.git@([^#]+)", conda_env).group(1)
    lr_reqs = re.search(r"LiquidsReflectometer\.git@([^#]+)", reqs_env).group(1)
    if lr_conda != lr_reqs:
        raise RuntimeError("environment.yml and requirements.txt ask different versions of LiquidsReflectometer")


if __name__ == "__main__":
    try:
        check_dependencies_synced()
    except RuntimeError as e:
        logging.error(f"{e}")
        sys.exit(1)
    sys.exit(0)
