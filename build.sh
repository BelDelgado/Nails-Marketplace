#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r nails-marketplace/project/requirements.txt

PYTHON_EXEC="python nails-marketplace/project/manage.py"

$PYTHON_EXEC collectstatic --no-input --clear