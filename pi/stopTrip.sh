#!/bin/bash
#written by Charlie Gleason
#Team AUTO May 2016

if [ "$(whoami)" != "root" ]
then
	printf "You need to be root to run this script"; exit 1
else
	killall python; exit 0
fi
