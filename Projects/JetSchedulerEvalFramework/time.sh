#!/usr/bin/env bash

start=`date +%s`

python3 Simulator.py

end=`date +%s`

result=$( expr ${end} - ${start} )
echo "$result seconds"