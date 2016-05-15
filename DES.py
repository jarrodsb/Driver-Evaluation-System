# Jarrod Bieber
# CAPSTONE Team Auto
# Driver Evaluation System

import testprog

#if __name__ == '__main__':

# As the Raspberry Pi is powered on (vehicle ignition), first evaluate 
# the OBD2 data from the previous driving session
testprog.dataEval()

# Then, in a continuous loop, start collecting data from the OBD2 reader
# and the GPS adapter. Convert the data into a CSV file that gets placed in
# the OBD_data folder. Do this until the vehicle is turned off.
# (call Charlie's script here)