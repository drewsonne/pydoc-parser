from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pydoc-parser',
    version='0.0.2',
    packages=['examples', 'pydocparser'],
    url='https://github.com/drewsonne/pydoc-parser/',
    license='LGPL3',
    author='Drew J. Sonne',
    author_email='drew.sonne@gmail.com',
    description='A python library to parse doc blocks from python modules',
    install_requires=[],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
