from distutils.core import setup;
from setuptools import find_packages
setup(name='OpenWPM',
      version='0.1.0',
      package_data = {'': ['*']},
      packages=find_packages(exclude=['OpenWPM.test']),
      )
