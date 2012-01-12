# -*- coding: utf-8 -*-

from distutils.core import setup

with open("README.txt") as f:
    long_description = f.read()

setup(name='epub',
      version='0.1.0',
      description='Library to open and read files in the epub version 2.',
      long_description=long_description,
      author='Florian Strzelecki',
      author_email='florian.strzelecki@gmail.com',
      license='LGPL',
      url='http://epub.exirel.me',
      packages=['epub',])
