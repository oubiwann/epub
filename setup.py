# -*- coding: utf-8 -*-

from distutils.core import setup


with open("README.txt") as f:
    long_description = f.read()


setup(name=u'epub',
      version=u'0.4.0',
      description=u'Library to open and read files in the epub version 2.',
      long_description=long_description,
      author=u'Florian Strzelecki',
      author_email=u'florian.strzelecki@gmail.com',
      license=u'LGPL',
      url=u'http://epub.exirel.me',
      packages=[u'epub'],
      classifiers=[u'Development Status :: 4 - Beta',
                  u'Intended Audience :: Developers',
                  u'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                  u'Programming Language :: Python :: 2.7',
                  u'Topic :: Software Development :: Libraries :: Python Modules'])
