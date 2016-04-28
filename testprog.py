import csv

counter = int(0)

# change these depending on where in the row of data the value is listed
speedcolm = 12
rpmcolm = 13
throttlecolm = 15
distcolm = 14
#mpgcolm = 16
timecolm = 0
latcolm = 3
longcolm = 2

# Latitude/Longitude grid
# *****************************************************************************

# 1 degree of latitude/longitude = roughly 100 sq kilometers
# 1000 intervals over 100 km = 100 meter intervals
gridinterval = 0.001
totalintervals = 1000

# 100 sq km grid based around my travel route
grid = {}
for y in range(0, totalintervals):
	for x in range (0, totalintervals):
		grid[((-76 + (gridinterval * x)),(40 - (gridinterval * y)))] = []
		
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

# open OBD2 data file
OBDdata = 'Thurs_2-25_Log.csv'
with open(OBDdata) as csvfile:
	readCSV = csv.reader(csvfile, delimiter=',')
	
	speeds = []
	rpms = []
	throttles = []
	dist = []
	gpslats = []
	gpslongs = []
	
	spdcount = 0
	brkcount = 0
	aclcount = 0
	
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
			# Need to average these values and come up with an acceptable deviation limit.
			if (speed != 0):
				grid[(round(gpslong, 3),round(gpslat, 3))].append(speed)
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
maxrmp = max(rpms)
maxthrottle = max(throttles)
	
# Calculate total score and grade
score = (spdcount + brkcount*2 + aclcount*2) / totaldist
if score == 0: grade = "A+"
elif score <= .5: grade = "A"
elif score <= 1: grade = "A-"
elif score <= 1.5: grade = "B+"
elif score <= 2: grade = "B"
elif score <= 2.5: grade = "B-"
elif score <= 3: grade = "C+"
elif score <= 3.5: grade = "C"
elif score <= 4: grade = "C-"
elif score <= 4.5: grade = "D+"
elif score <= 5: grade = "D"
elif score <= 5.5: grade = "D-"
else: grade = "F"


# print "report"
print("******************************REPORT******************************")
print("Your trip began at this time:", tripdate)
print ("On this trip you traveled", totaldist, "miles from (",
	gpslongs[0], ",", gpslats[0], ")\n", "to (", gpslongs[len(gpslongs)-1], ",", gpslats[len(gpslats)-1], ") in ", totalmin, "minutes")
print ("Max engine RPM for this trip was", maxrmp)
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
print ("FINAL GRADE:", grade)
	
	