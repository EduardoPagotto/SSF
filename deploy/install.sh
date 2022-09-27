#!/bin/sh
pip3 install -r requirements.txt
tar xvf SSF-1.0.1.tar.gz
cd SSF-1.0.1/
python3 setup.py install
cd ..
