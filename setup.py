import os
from setuptools import setup




setup(name='arxivtools',
      version='0.0.2',
      author='InAKleinBottle',
      packages=['arxivtools'],
      install_requires=['scipy',
                        'scikit-learn',
                        'appdirs',
                        'html5lib',
                        'beautifulsoup4',
                        'feedparser',
                        'requests',
		        'click'
                       ],
      entry_points={'console_scripts' : ['arxivdaily=arxivtools:daily_search',
					 'arxivtools=arxivtools.cli:arxivtools']},
      )


import appdirs
OUTPUT_DIR = os.path.expanduser(os.path.join('~', 'arxiv'))
APP_CONF_DIR = appdirs.user_data_dir('arxivtools', '')



if not os.path.exists(OUTPUT_DIR):  
    os.makedirs(OUTPUT_DIR)
if not os.path.exists(APP_CONF_DIR):
    os.makedirs(os.path.join(APP_CONF_DIR, 'data', 'pos'))
    os.makedirs(os.path.join(APP_CONF_DIR, 'data', 'neg'))
