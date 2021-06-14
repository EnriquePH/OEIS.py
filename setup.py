#!/usr/bin/env python3

from setuptools import setup

setup(
    name='oeis',
    url='https://oeis.org/',
    author='Enrique Pérez Herrero',
    author_email='eph.project1500@gmail.com',
    # Needed to actually package something
    #packages=['btc'],
    # Needed for dependencies
    #install_requires=['numpy', 'pandas', 'bs4'],
    # *strongly* suggested for sharing
    version='0.0.1.1',
    license='LICENSE',
    include_package_data=True,
    packages=['oeis'],
    description='Data from The On-Line Encyclopedia of Integer Sequences in Python',
)