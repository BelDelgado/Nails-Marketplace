#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip
pip install -r nails-marketplace/project/requirements.txt

PYTHON_EXEC="python nails-marketplace/project/manage.py"

$PYTHON_EXEC collectstatic --no-input
$PYTHON_EXEC migrate