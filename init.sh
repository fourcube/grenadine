#!/bin/bash
which pip > /dev/null

if [ $? -gt 0 ]; then
    sudo apt-get install python-dev
    wget https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py
    python get-pip.py
else
    echo "pip already installed"
fi

pip install flask


