#!/bin/bash

echo " Apply database Migration "

python manage.py migrate

exec"$@"