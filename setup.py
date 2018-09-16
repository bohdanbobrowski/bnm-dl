# coding=utf-8
#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# Autor: Bohdan Bobrowski bohdan@bobrowski.com.pl

from setuptools import setup

setup(
    name='bnm-dl',
    version='0.3',
    description=u'Proste pobieranie pobieranie filmów z cyklu "Było... nie minęło. Kronika zwiadowców historii"',
    url="https://github.com/bohdanbobrowski/BnmDl",
    author="Bohdan Bobrowski",
    author_email="bohdanbobrowski@gmail.com",
    license="MIT",
    packages=[
        "bnmdl"
    ],
    install_requires=[
        "lxml",
        "pycurl",
        "download"
    ],
    entry_points={
        'console_scripts': [
            'bnmdl = bnmdl.BnmDlCli:main',
        ]
    },
)
