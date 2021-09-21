import os
from setuptools import setup
import versioneer

THIS_DIR = os.path.dirname(__file__)


def read_requirements_from_file(filepath):
    r"""Read a list of dependencies from the given file and split into a list.

    It is assumed that the file is a flat list with one requirement per line.

    :param str filepath: Path to the file to read
    :return List[str]:
    """
    with open(filepath, 'rU') as req_file:
        return req_file.readlines()


install_requires = read_requirements_from_file(
    os.path.join(THIS_DIR, 'requirements.txt')
)
test_requires = read_requirements_from_file(
    os.path.join(THIS_DIR, 'requirements_dev.txt')
)

# TODO can this be safely substituted with setuptools.find_packages?
__packages__ = ['RefRed',
                'RefRed.autopopulatemaintable',
                'RefRed.configuration',
                'RefRed.clocking_algorithms',
                'RefRed.calculations',
                'RefRed.config',
                'RefRed.export',
                'RefRed.gui_handling',
                'RefRed.initialization',
                'RefRed.interfaces',
                'RefRed.load_reduced_data_set',
                'RefRed.low_res_finder_algorithms',
                'RefRed.metadata',
                'RefRed.peak_finder_algorithms',
                'RefRed.plot',
                'RefRed.preview_config',
                'RefRed.reduction',
                'RefRed.reduction_table_handling',
                'RefRed.settings',
                'RefRed.sf_calculator',
                'RefRed.sf_preview',
                'RefRed.thread',
                ]

setup(name='RefRed',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description='Liquids Reflectrometer Data Reduction Software',
      license='GPL version 3.0',
      scripts=['scripts/RefRed', 'scripts/start_refred.py'],
      author='Jean Bilheux',
      author_email='bilheuxjm@ornl.gov',
      packages=__packages__,
      url='http://',
      zip_safe=False,
      package_dir={},
      install_requires=install_requires,
      setup_requires=["pytest-runner"],
      tests_require=test_requires,
      )
