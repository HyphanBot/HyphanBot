#!/bin/bash

# HyphanBot's Launch Script

# Function to get the absolute path of a relative path
#function getAbsPath() {(
#cd $(dirname $1)         # or  cd ${1%/*}
#echo $PWD/$(basename $1) # or  echo $PWD/${1##*/}
#)}

# HyphanBot's root directory should be this script's parent directory
export HYPHAN_DIR=$(pwd)
python3 "main.py" "$@"
