#!/bin/bash
export FLASK_APP="web.py"
if [ -n $1 ]; then
	cd $1
else
	cd .
fi
. ./bin/activate
cd app
printf "\e[96m\e[1m"
echo "=== $(realpath ./) ==="
echo "=== Running $0 ==="
echo "=== FLASK_APP = $FLASK_APP ==="
printf "\e[0m\e[39m"
flask run
