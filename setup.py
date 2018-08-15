from setuptools import setup




setup(name='arxivtools',
      version='0.0.2',
      author='InAKleinBottle',
      packages=['arxivtools'],
      setup_requires=['scipy',
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
