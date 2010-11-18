import os
from setuptools import setup
from  cofre import __version__ as version

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "cofre",
    version = version,
    author = "Rafael Ferreira",
    author_email = "raf@ophion.org",
    description = ('Public key based password manager'),
    license =  'MIT/X11',
    keywords = "password encryption rsa",
    url = "https://github.com/rferreira/cofre",
    packages=['cofre'],
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 4 - Beta',
        "Topic :: Utilities",
        'License :: OSI Approved :: Apple Public Source License'
    ],
    install_requires=['M2Crypto','prettytable'],
    scripts=['scripts/cofre']
)
