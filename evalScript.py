# Jarrod Bieber
# CAPSTONE Team Auto
# Driver Evaluation System

import csv
import glob
import shutil
import sqlite3
import pickle
from gridScript import grid

# These values depend on where their corresponding column is located in the the file
speedcolm = 12
rpmcolm = 13
throttlecolm = 15
distcolm = 14
#mpgcolm = 16
timecolm = 0
latcolm = 3
longcolm = 2

# Database
# ****************************************************************************

conn = sqlite3.connect('grid.db')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS speedAverages(datetime TEXT, coordinate_area TEXT, speedavg REAL)')

def data_entry(date, key, list):
	spdavg = avg(list)
	c.execute("INSERT INTO speedAverages(datetime, coordinate_area, speedavg) VALUES (?, ?, ?)",(date, str(key), spdavg))
	

# Latitude/Longitude grid
# *****************************************************************************

# 1 degree of latitude/longitude = roughly 100 sq kilometers
# 1000 intervals over 100 km = 100 meter intervals
# gridinterval = 0.001
# totalintervals = 1000

# 100 sq km grid based around my travel route
# grid = {}
# for y in range(0, totalintervals):
	# for x in range (0, totalintervals):
		# grid[((-76 + (gridinterval * x)),(40 - (gridinterval * y)))] = []
		
# ******************************************************************************

# checks if the string value can be converted into a number.
# If not, returns 0
def is_number(s):
    try:
        float(s)
        return s
    except ValueError:
        return 0
		
# functions for finding the average speed within a square
# and determining if speeding
def avg(list):
	return (round(sum(list)/len(list), 2))

def is_speeding(list,num):
	if (len(list) >= 30 and num >= (avg(list) + 15)) or num >= 70:
		return True
	else:
		return False

# Main function
def dataEval():
	
	# ************Load the first CSV file it sees in "OBD_Data" directory***********
	for filename in glob.glob('*.csv'): # using Glob

		counter = int(0)
			
		speeds = []
		rpms = []
		throttles = []
		dist = []
		gpslats = []
		gpslongs = []
		
		spdcount = 0
		brkcount = 0
		aclcount = 0
		
		# Parse through file and extract information using csv module
		with open(filename) as csvfile:
			readCSV = csv.reader(csvfile, delimiter=',')
			
			# parse through file
			for row in readCSV:
				# skips the first two rows
				if counter < 2:
					if counter > 0:
						tripdate = row[timecolm]
					counter += 1
				else:
					speed = round(float(is_number(row[speedcolm])), 2)
					rpm = float((is_number(row[rpmcolm])))
					throttlepos = round(float(is_number(row[throttlecolm])), 2)
					currentdist = round(float(is_number(row[distcolm])), 2)
					gpslat = float(is_number(row[latcolm]))
					gpslong = float(is_number(row[longcolm]))
					
					speeds.append(speed)
					rpms.append(rpm)
					throttles.append(throttlepos)
					dist.append(currentdist)
					gpslats.append(gpslat)
					gpslongs.append(gpslong)
					
					
					# The value of each key is a list of speeds.
					# These speeds are the collected logged speeds for that square.
					if (speed != 0):
						if  (round(gpslong, 3),round(gpslat, 3)) in grid:
							grid[(round(gpslong, 3),round(gpslat, 3))].append(speed)
						else:
							grid[(round(gpslong, 3),round(gpslat, 3))] = [speed]
						
						if is_speeding(grid[(round(gpslong, 3),round(gpslat, 3))], speed):
							if speed > speeds[len(speeds)-2]:
								# if gpslongs[len(gpslongs)-1] != gpslongs[len(gpslongs)-2]:
									# if gpslats[len(gpslats)-1] != gpslats[len(gpslats)-2]:
								spdcount = spdcount + 1
								print("Potential speeding at (", gpslong, ",", gpslat, ")")
								print("The calculated average was", avg(grid[(round(gpslong, 3),round(gpslat, 3))]), "mph")
								print("You were going", speed, "mph\n")
							
					
					# Check for acceleration
					if len(speeds) > 10 and speed-speeds[len(speeds)-11] > 6:
						if gpslong != gpslongs[len(gpslongs)-2] or gpslat != gpslats[len(gpslats)-2]:
							print("Aggressive acceleration at (", gpslong, ",", gpslat, ")\n")
							aclcount = aclcount + 1
					
					# Check for breaking
					if len(speeds) > 10 and speed-speeds[len(speeds)-11] < -6:
						if gpslong != gpslongs[len(gpslongs)-2] or gpslat != gpslats[len(gpslats)-2]:
							print("Aggressive breaking at (", gpslong, ",", gpslat, ")\n")
							brkcount = brkcount + 1
		
		# calculate distance and time
		totaldist = max(dist)
		totalsec = len(dist)/10 # divide by 2 for half-seconds, divide by 10 for 0.1 seconds
								# multiply by 2 if recorded every 2 seconds, etc
		totalmin = round(totalsec/60, 2)
		
		# calculate max speed, rpm and throttle
		maxspd = max(speeds)
		maxrpm = max(rpms)
		maxthrottle = max(throttles)
			
		# Calculate total score and grade (needs tweaking)
		score = (spdcount + brkcount*3 + aclcount*3) / totaldist
		if score == 0: grade = "A+"
		elif score <= 2.5: grade = "A"
		elif score <= 3: grade = "A-"
		elif score <= 3.5: grade = "B+"
		elif score <= 4: grade = "B"
		elif score <= 4.5: grade = "B-"
		elif score <= 5: grade = "C+"
		elif score <= 5.5: grade = "C"
		elif score <= 6: grade = "C-"
		elif score <= 6.5: grade = "D+"
		elif score <= 7: grade = "D"
		elif score <= 7.5: grade = "D-"
		else: grade = "F"


		# print report to console
		print("******************************REPORT******************************")
		print("Your trip began at this time:", tripdate)
		print ("On this trip you travelled", totaldist, "miles from (",
			gpslongs[0], ",", gpslats[0], ")\n", "to (", gpslongs[len(gpslongs)-1], ",", gpslats[len(gpslats)-1], ") in ", totalmin, "minutes")
		print ("Max engine RPM for this trip was", maxrpm)
		print ("Max throttle position for this trip was", maxthrottle, "%")
		if maxthrottle > 70:
			print ("**You're flooring it!**")
		print ("Max speed for this trip was", maxspd, "mph")
		if spdcount > 0:
			print("Detected", spdcount, "instances of potential speeding!")
		if brkcount > 0:
			print("Detected", brkcount, "instances of sharp breaking!")
		if aclcount > 0:
			print("Detected", aclcount, "instances of sharp acceleration!")
		print("")
		print ("FINAL GRADE:", grade, "\n")
		print("******************************************************************")
		
		# Write report to text file (add it to the other reports)
		report = open('Reports.txt','a')
		report.write('***************************************************************\n')
		report.write('Your trip began at this time: ' + tripdate + '\n')
		report.write("On this trip you travelled " + str(totaldist) + " miles\nfrom (" 
			+ str(gpslongs[0]) + "," + str(gpslats[0]) + ") " + "to ("
			+ str(gpslongs[len(gpslongs)-1]) + "," + str(gpslats[len(gpslats)-1])
			+ ") in " + str(totalmin) + " minutes\n")
		report.write("Max engine RPM for this trip was " + str(maxrpm) + "\n")
		report.write("Max throttle position for this trip was " + str(maxthrottle) + "%\n")
		if maxthrottle > 70:
			report.write("**You're flooring it!**\n")
		report.write("Max speed for this trip was " + str(maxspd) + " mph\n")
		if spdcount > 0:
			report.write("Detected " + str(spdcount) + " instances of potential speeding!\n")
		if brkcount > 0:
			report.write("Detected " + str(brkcount) + " instances of sharp breaking!\n")
		if aclcount > 0:
			report.write("Detected " + str(aclcount) + " instances of sharp acceleration!\n")
		report.write("\nFINAL GRADE: " + grade + "\n\n")
		report.close()
		
		# Remove used CSV files from the directory using Shutil
		# The paths will have to change if we get it on a Pi
		srcpath = ("C:\\Users\\Jarrod\\Documents\\School Files\\SENIOR DESIGN\\CSV-files\\OBD_data\\" + filename)
		destpath = ("C:\\Users\\Jarrod\\Documents\\School Files\\SENIOR DESIGN\\CSV-files\\Used_files\\" + filename)
		shutil.move(srcpath,destpath)
		# ******************End CSV file, go to new one if there are any**************
	
	# Update the grid with new data usingle Pickle
	pickle_out = open("grid.pickle", "wb")
	pickle.dump(grid,pickle_out)
	pickle_out.close()
	
	# put speed averages into database
	for key in grid:
		data_entry(tripdate, key, grid[key])
	
	# Close database
	conn.commit()
	c.close()
	conn.close()
	