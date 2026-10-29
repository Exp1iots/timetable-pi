#!/bin/bash

cd /home/user/timetable-pi || exit 1

.venv/bin/python main.py "$@"