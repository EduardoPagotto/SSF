#!/bin/sh
pip3 install -r requirements.txt
tar xvf SSF-0.0.1.tar.gz
cd SSF-0.0.1/
python3 setup.py install
cd ..
