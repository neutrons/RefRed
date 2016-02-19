from distutils.core import setup
from RefRed.version import str_version

__package_name__ = 'RefRed'
__version__ = str_version
__description__ = 'Liquids Reflectrometer Data Reduction Software'
__author__ = 'Jean Bilheux'
__author_email__ = 'bilheuxjm@ornl.gov'
__license__ = 'Copyright 2015-2016'
__url__ = 'http://'
__scripts__ = ['scripts/RefRed']
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

setup(name = __package_name__,
      version = __version__,
      description = __description__,
      scripts = __scripts__,
      author = __author__,
      author_email = __author_email__,
      packages = __packages__,
      url = __url__)
