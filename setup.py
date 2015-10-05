#!/usr/bin/env python

from setuptools import setup

setup(
    name='tildetown',
    version='0.0.1',
    description='python stuf for tilde.town',
    url='https://github.com/tildetown/tildetown-scripts',
    author='vilmibm shaksfrpease',
    author_email='nks@lambdaphil.es',
    license='GPL',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Other Audience',
        'Topic :: Artistic Software',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
    ],
    keywords='community',
    packages=['tildetown'],
    install_requires = ['pyhocon==0.3.10', 'sh==1.11', 'Flask==0.10.1', 'requests==2.7.0'],
)
