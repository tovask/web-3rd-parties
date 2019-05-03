from distutils.core import setup;
from setuptools import find_packages
import os

setup(name='OpenWPM',
      version='0.1.0',
      packages=find_packages(exclude=['OpenWPM.test']),
      package_data = {'OpenWPM': [ os.path.join(root[len('OpenWPM/'):],filename) for root, dirs, files in os.walk ("OpenWPM") for filename in files ] },
    )
