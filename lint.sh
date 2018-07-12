#!/bin/bash

# SYNC: Keep this in sync with lint-settings.vim
flake8                           \
    --exclude=local_settings.py  \
    --jobs=4                     \
    --ignore=E124,E126,E128,E131,E156,E201,E221,E222,E225,E241,E251,E265,E271,E272,E501,E701,F405,W503

# Find all subdirectories of a Django app and use xargs to pass them as arguments to pylint
find e_munchkin/ users/ -maxdepth 1 -mindepth 1 -type d   \
    | grep --invert-match --regexp '^.*__pycache__.*' \
    | xargs pylint --rcfile=pylintrc

read $CMD
