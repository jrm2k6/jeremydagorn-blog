#!/bin/bash

sudo apt-get update
sudo apt-get install python-pip python-dev nginx virtualenv libxml2-dev libxslt1-dev zlib1g-dev lxml uwsgi nodejs npm
sudo npm install -g less
sudo ln -s /usr/bin/nodejs /usr/bin/node
sudo apt-get install python-pip python-dev nginx

sudo pip install virtualenv
pip install uwsgi flask
