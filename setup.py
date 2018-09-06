# coding=utf-8
#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# Autor: Bohdan Bobrowski bohdan@bobrowski.com.pl

from setuptools import setup

setup(
    name='BnmDl',
    version='0.1',
    description=u'Proste pobieranie pobieranie filmów z cyklu "Było... nie minęło. Kronika zwiadowców historii"',
    url="https://github.com/bohdanbobrowski/BnmDl",
    author="Bohdan Bobrowski",
    author_email="bohdanbobrowski@gmail.com",
    license="MIT",
    packages=[
        "BnmDl"
    ],
    install_requires=[
        "lxml",
        "urllib2",
        "pycurl"
    ],
    entry_points={
        'console_scripts': [
            'bnmdl = BnmDl.BnmDlCli:main',
        ]
    },
)