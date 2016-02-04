from __future__ import unicode_literals

from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='geog',
    version='0.0.2',
    description="Numpy-based vectorized geospatial functions",
    long_description=long_description,
    classifiers=[],
    keywords='',
    author="Jacob Wasserman",
    author_email='jwasserman@gmail.com',
    url='https://github.com/jwass/geog',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'numpy',
    ],
    extras_require={
        'test': ['pytest', 'tox'],
    },
)
