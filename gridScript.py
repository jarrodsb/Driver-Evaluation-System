# Jarrod Bieber
# CAPSTONE Team Auto
# Driver Evaluation System

import pickle
import os.path
		
		
if 	os.path.isfile("grid.pickle"):
	pickle_in = open("grid.pickle","rb")
	grid = pickle.load(pickle_in)
else:
	grid = {}