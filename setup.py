from distutils.core import setup
from RefRed.version import str_version


__package_name__ = "RefRed"
__version__ = str_version
__description__ = "Liquids Reflectrometer Data Reduction Software"
__author__ = 'Jean Bilheux'
__author_email__ = "bilheuxjm@ornl.gov"
__license__ = "Copyright 2015-2016"
__url__ = "http://"
__scripts__ = 'scripts/quicknxsl'
__packages__ = ['RefRed']
__package_dir__ = {'RefRed': ['autopopulatemaintable',
                   'calculations',
                   'config',
                   'configuration',
                   'export',
                   'genx_templates',
                   'gui_handling',
                   'htmldoc', 
                   'initialization',
                   'interfaces',
                   'peak_finder_algorithms',
                   'plot',
                   'reduction',
                   'reduction_table_handling',
                   'sf_calculator',
                   'thread']}

setup(name = __package_name__,
      version = __version__,
      description = __description__,
      scripts = __scripts__,
      author = __author__,
      author_email = __author_email__,
      packages = __packages__,
      url = __url__)
