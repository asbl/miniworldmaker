from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))


# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') \
        as f:long_description = f.read()

setup(name='gamegridp',
      version='0.9',
      description='An educational 2D Engine for Python',
      long_description=long_description,
      long_description_content_type='text/markdown',
      keywords=['game', 'education'],  # arbitrary keywords
      author='Andreas Siebel',
      author_email='andreas.siebel@it-teaching.de',
      url='https://github.com/asbl/gamegridp',
      download_url='https://github.com/asbl/gamegridp',
      license="OSI Approved :: MIT License",
      classifiers=["License :: OSI Approved :: MIT License",
                   "Programming Language :: Python",
                   "Development Status :: 4 - Beta",
                   "Intended Audience :: Education",
                   "Topic :: Education",
                   ],
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
      package_data={'game_grid': ['data/*.png']},
      install_requires=['pygame', 'easygui'],
      )