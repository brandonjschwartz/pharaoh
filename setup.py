import os
import sys

from setuptools import setup, find_packages

py_version = sys.version_info[:2]

PY3 = py_version[0] == 3

if PY3:
    if py_version < (3, 2):
        raise RuntimeError('On Python 3, Pharaoh requires Python 3.2 or better')
else:
    if py_version < (2, 6):
        raise RuntimeError('On Python 2, Pharaoh requires Python 2.6 or better')

here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, 'README.txt')) as f:
        README = f.read()
    with open(os.path.join(here, 'CHANGES.txt')) as f:
        CHANGES = f.read()
except IOError:
    README = CHANGES = ''

install_requires = [
    'setuptools',
    'pyramid',
]


tests_require = [
    'nose',
    'nose-selecttests',
    'coverage',
    'virtualenv', # for starter package tests
]

setup(name='pharaoh',
      version='0.0.1',
      description=('Pharaoh command line tool'),
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "License :: Repoze Public License",
      ],
      keywords='web wsgi pylons pyramid',
      author="Brandon J. Schwartz",
      author_email="brandon@boomajoom.com",
      url="http://www.boomajoom.com",
      license="MIT",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires = install_requires,
      tests_require = tests_require,
      test_suite="pyramid.tests",
      entry_points = """\
        [pharaoh.starter_package]
        sqlalchemy=pharaoh.starter_packages:SqlAlchemyPkg
        [console_scripts]
        pharaoh = pharaoh.scripts.pharaoh:main
      """
      )
