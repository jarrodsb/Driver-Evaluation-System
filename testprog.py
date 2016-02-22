import csv

counter = 0

# change these depending on where in the row of data the value is listed
speedcolm = 13
rpmcolm = 12
throttlecolm = 14
distcolm = 15
mpgcolm = 16
timecolm = 0

# checks if the string value can be converted into a number.
# If not, returns 0
def is_number(s):
    try:
        float(s)
        return s
    except ValueError:
        return 0

# open file
with open('Thurs12-3Log.csv') as csvfile:
	readCSV = csv.reader(csvfile, delimiter=',')
	
	speeds = []
	rpms = []
	throttles = []
	dist = []
	mpgs = []
	
	# parse through file
	for row in readCSV:
		
		# skips the first two rows
		if counter < 2:
			if counter > 0:
				tripdate = row[timecolm]
			counter += 1
		else:
			speed = round(float(row[speedcolm]), 2)
			rpm = float(row[rpmcolm])
			throttlepos = round(float(row[throttlecolm]), 2)
			currentdist = round(float(row[distcolm]), 2)
			mpg = round(float(is_number(row[mpgcolm])), 2)
			
			speeds.append(speed)
			rpms.append(rpm)
			throttles.append(throttlepos)
			dist.append(currentdist)
			mpgs.append(mpg)
	
	# calculate distance and time
	totaldist = max(dist)
	totalsec = len(dist)/2 # divide by 2 for half-seconds, divide by 10 for 0.1 seconds
							# multiply by 2 if recorded every 2 seconds, etc
	totalmin = round(totalsec/60, 2)
	
	# calculate max speed, rpm and throttle
	maxspd = max(speeds)
	maxrmp = max(rpms)
	maxthrottle = max(throttles)
	
	# calculate average mpg
	avgmpg = round(sum(mpgs)/len(mpgs), 2)
	
	# print "report"
	print ("\nYour trip began at this time:", tripdate)
	print ("On this trip you traveled", totaldist, "miles in", totalmin, "minutes\n")
	print ("Max speed for this trip was", maxspd, "mph")
	if maxspd > 65:
		print("- **You're speeding!**")
	else: print ("")
	print ("Max engine RPM for this trip was", maxrmp)
	print ("Max throttle position for this trip was", maxthrottle, "%")
	if maxthrottle > 70:
		print ("You're flooring it!")
	print ("Your average miles per gallon was", avgmpg)
	
