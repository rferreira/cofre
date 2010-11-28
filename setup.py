import os
from setuptools import setup
from  cofre import __version__ as version
setup(
    name = "cofre",
    version = version,
    author = "Rafael Ferreira",
    author_email = "raf@ophion.org",
    description = ('the serendipitous password manager'),
    license =  'MIT/X11',
    keywords = "password encryption rsa",
    url = "https://github.com/rferreira/cofre",
    packages=['cofre'],
    long_description='simple and secure password manager that utilizes your ssh keys',
    classifiers=[
        'Development Status :: 4 - Beta',
        "Topic :: Utilities",
        'License :: OSI Approved :: Apache Software License'
    ],
    install_requires=['M2Crypto','prettytable'],
    scripts=['scripts/cofre']
)
