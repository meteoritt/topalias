#!/bin/bash

# License GPLv3 #__# $5 default alias counter 30

# Install requirements
#sudo apt install python3 python3-pip -y

# Install from pypi.org
#pip3 install -U --user topalias

# Run python script

python3 topalias/cli.py $@

echo "Report you great ideas and any feedback: https://github.com/CSRedRat/topalias/issues/new"
