#!/bin/bash

# If deps are installed exit gracefully.
which python2.6 && \
which python2.7 && \
which python3.2 && \
which python3.3 && \
which python3.4 && \
which jython && \
which pypy && \
exit 0

# Add deadsnakes ppa https://launchpad.net/~fkrull/+archive/deadsnakes .
apt-get update
apt-get install -y python-software-properties
add-apt-repository -y ppa:fkrull/deadsnakes
apt-get update

# Install all supported python version.
apt-get install -y python2.6 python2.7 python3.1 python3.2 python3.3 python3.4 jython pypy

# Install the development dependencies.
apt-get install -y python-pip
pip install -r /vagrant/requirements/develop.txt
