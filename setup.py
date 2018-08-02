from setuptools import setup




setup(name='arxivtools',
      version='0.0.1',
      author='InAKleinBottle',
      packages=['arxivtools'],
      setup_requires=['scikit-learn',
                      'appdirs',
                      'beautifulsoup4',
                      'feedparser',
                      'requests',
                      ]
      )
                      
