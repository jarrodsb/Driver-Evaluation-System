# Jarrod Bieber
# CAPSTONE Team Auto
# Driver Evaluation System

import pickle
import os.path

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
		
		
if 	os.path.isfile("grid.pickle"):
	pickle_in = open("grid.pickle","rb")
	grid = pickle.load(pickle_in)
else:
	grid = {}