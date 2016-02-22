#OBD2 Module GUI
#Senior Design

from tkinter import*
from math import*
import csv



class OBD2(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.csv_read()

    def is_number(self, s):
        try:
            float(s)
            return s
        except ValueError:
            return 0

    def csv_read(self):
        with open('Thurs12-3Log.csv') as csvfile:
            counter = 0
            speedcolm = 13
            rpmcolm = 12
            throttlecolm = 14
            distcolm = 15
            mpgcolm = 16
            timecolm = 0
            readCSV = csv.reader(csvfile, delimiter = ',')
            speeds = []
            rpms = []
            throttles = []
            dist = []
            mpgs =[]

            for row in readCSV:
                if counter < 2:
                    if counter > 0:
                        tripdate = row[timecolm]
                    counter += 1
                else:
                    speed = round(float(row[speedcolm]), 2)
                    rpm = float(row[rpmcolm])
                    throttlepos = round(float(row[throttlecolm]), 2)
                    currentdist = round (float(row[distcolm]),2)
                    mpg = round(float(self.is_number(row[mpgcolm])), 2)

                    speeds.append(speed)
                    rpms.append(rpm)
                    throttles.append(throttlepos)
                    dist.append(currentdist)
                    mpgs.append(mpg)
                                
            totaldist = max(dist)
            totalsec = len(dist)/2

            totalmin = round(totalsec/60, 2)

            maxspd = max(speeds)
            maxrmp = max(rpms)
            maxthrottle = max(throttles)

            avgmpg = round(sum(mpgs)/len(mpgs), 2)
            self.text = Text(self, height = 10, width = 40)
            self.text.grid()
            message1 = "\nYour trip began at this time: " + str(tripdate)
            self.text.insert(0.0, message1)
            message2 = "\nOn this trip you traveled " + str(totaldist) + " miles in " + str(totalmin) + " minutes"
            self.text.insert(0.0, message2)
            message3 = "\nMax speed for this trip was " + str(maxspd) + " mph"
            self.text.insert(0.0, message3)
            if maxspd > 65:
                message4 = "\n- **You're speeding!**"
            else:
                message4 = ""
            self.text.insert(0.0, message4)
            message5 = "\nMax engine RPM for this trip was " + str(maxrmp)
            self.text.insert(0.0, message5)
            message6 = "\nMax throttle position for this trip was " + str(maxthrottle) + " %"
            self.text.insert(0.0, message6)
            if maxthrottle > 70:
                message7 = "\nYou're flooring it!"
                self.text.insert(0.0, message7)
            message8 = "\nYour average miles per gallon was " + str(avgmpg)

root = Tk()
root.title("OBD2 GUI")
root.geometry("1000x720")
app = OBD2(root)
root.mainloop()
