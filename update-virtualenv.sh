#!/bin/bash

. env/bin/activate

not_in_env_error() {
    echo "You are not in a virtualenv, please activate it like this:"
    echo " $ source virtualenv/bin/activate"
    exit 1
}

[ -z "${VIRTUAL_ENV}" ] && not_in_env_error

pip install  -r requirements.txt
deactivate
