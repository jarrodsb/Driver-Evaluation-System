#!/bin/bash
#written by Charlie Gleason
#Team AUTO May 2016

#create new log file
#create log folder if it doesn't exist

mkdir -p log
FILENAME="gpsdData_$(date +"%F_%T").log"
touch "log/$FILENAME"

#connect gpsd to GPS device's serial port and set socket file
#if gpsd setup succeeds, run python script and record data, running in background and ignoring interrupts
#to keep process running after ssh disconnect

if [ "$(whoami)" != "root" ]
then
	printf "You need to be root to run this script"; exit 1
else
	gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock && nohup python gpsdData.py > gpsdData.log &
fi
