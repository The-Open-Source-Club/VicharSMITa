#!/bin/bash
which python3.8 1>/dev/null
if [ $? -eq 1 ]; then
	PYTHON_EXEC="python3"
else
	PYTHON_EXEC="python3.8"
fi
$PYTHON_EXEC -m venv .
. bin/activate
$PYTHON_EXEC -m pip install -U pip
$PYTHON_EXEC -m pip install flask flask-wtf flask-sqlalchemy flask-login flask-migrate
