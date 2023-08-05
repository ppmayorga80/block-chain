#!/usr/bin/env bash

if [ ! -d venv ]; then
  echo "Creating venv"
  python3 -m venv venv
fi

source venv/bin/activate

if [[ ! $PYTHONPATH =~ $PWD ]]; then
  echo "Exporting PYTHONPATH"
  export PYTHONPATH=$PWD:$PYTHONPATH
fi

pip install --upgrade pip
pip install pipenv
pip install -r requirements.txt
