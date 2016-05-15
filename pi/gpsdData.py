#! /usr/bin/python
# Written by Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0
# Modified by Charlie Gleason May 2016
 
import os
from gps import *
from time import *
import time
import threading
 
gpsd = None #seting the global variable
 
#os.system('clear') #clear the terminal (optional)

f = open('gpsdData.log','w')
 
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
 
if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start() # start it up
    while True:
      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
 
      #os.system('clear')
       print gpsd.fix.latitude,', ',gpsd.fix.longitude,', ',gpsd.utc,' + ',gpsd.fix.time,', ',gpsd.fix.altitude,', ',gpsd.fix.eps,', ',gpsd.fix.epv,', ',gpsd.fix.ept,', ',gpsd.fix.speed,', ',gpsd.fix.climb,', ',gpsd.fix.track,', ',gpsd.fix.mode
      
       #f.write(', '.join(str(gpsd.fix.latitude, gpsd.fix.longitude, gpsd.utc,gpsd.fix.time, gpsd.fix.altitude, gpsd.fix.eps, gpsd.fix.epv, gpsd.fix.ept, gpsd.fix.speed, gpsd.fix.climb, gpsd.fix.track, gpsd.fix.mode)))

       time.sleep(1) #set to whatever
 
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    #print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  
  f.write("Done")
  f.close() 
#  print "Done.\nExiting."
