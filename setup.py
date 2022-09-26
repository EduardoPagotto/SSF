#!./venv/bin/python3
'''
Created on 20190821
Update on 20220922
@author: Eduardo Pagotto
'''

from setuptools import setup, find_packages

from RPC.__init__ import __version__ as VERSION

PACKAGE = "SSF"

# listar os packages
#python -c "from setuptools import setup, find_packages; print(find_packages())"

setup(
    name="SSF",
    version=VERSION,
    author="Eduardo Pagotto",
    author_email="edupagotto@gmail.com",
    description="SimpleStore File Server",
    long_description="Server to store temporary files using only index",#long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EduardoPagotto/SSF.git",
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=['typed-ast','typing-extensions', 'wheel', 'tinydb'],
)
