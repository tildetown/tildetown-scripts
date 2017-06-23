#!/usr/bin/env python

from setuptools import setup

setup(
    name='tildetown',
    version='1.0.2',
    description='executable scripts used on tildetown',
    url='https://github.com/tildetown/tildetown-scripts',
    author='vilmibm',
    author_email='tildetown@protonmail.ch',
    license='GPL',
    classifiers=[
        'Development Status :: 3 - Beta',
        'Intended Audience :: Other Audience',
        'Topic :: Artistic Software',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    include_package_data=True,
    keywords='community',
    packages=['tildetown'],
    install_requires = ['pystache==0.5.4'],
    entry_points = {
          'console_scripts': [
              'stats = tildetown.stats:main',
              'mustache = tildetown.__init__:mustache',
              'generate_homepage = tildetown.__init__:generate_homepage',
          ]
    },
)
