#!/bin/bash

set -e

SCRIPTS_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
REPO_DIR="$SCRIPTS_DIR/.."
VENV_DIR="$REPO_DIR/venv"
INTERPRETER_PATH="$REPO_DIR/venv/bin/python3"

python3 -m venv $VENV_DIR
$INTERPRETER_PATH -m pip install -r $REPO_DIR/requirements.txt
