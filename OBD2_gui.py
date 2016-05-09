#OBD2 Module GUI
#Senior Design

from tkinter import*
from math import*
import csv



class OBD2(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.openingWidget()
        self.buttonPressed = 0 #to make sure Show me result button is only pressed once //for now

    #To determine what to do when a button is pressed
    def OnButtonClick(self, button_id):
        if button_id == 1:
            if self.buttonPressed == 0:
                self.csv_read()
                self.buttonPressed = 1
                
        elif button_id == 2:
            self.clearGui()
            self.createMainWidget()
            self.buttonPressed = 0

        elif button_id == 3:
            self.clearGui()
            self.createMainWidget()

        elif button_id == 4:
            self.clearGui()
            self.openingWidget()
            if(self.buttonPressed == 1):
                self.buttonPressed = 0

    #Create Opening Widgets
    def openingWidget(self):
        self.label1 = Label(self, text = "OBD2 Data Analysis")
        self.label1.grid()
        self.button1 = Button(self, text = "Start", command = lambda:self.OnButtonClick(3))
        self.button1.grid()
        
    #Create Main Widgets        
    def createMainWidget(self):
        self.button1 = Button(self, text = "Show Result", command = lambda:self.OnButtonClick(1))
        self.button1.grid()
        self.button2 = Button(self, text = "Reset", command = lambda:self.OnButtonClick(2))
        self.button2.grid()
        self.button3 = Button(self, text = "Back", command = lambda: self.OnButtonClick(4))
        self.button3.grid()


    #To clear the frame of the widgets but don't destroy the frame
    def clearGui(self):
       for widget in Frame.winfo_children(self):
           widget.destroy()



    def is_number(self, s):
        try:
            float(s)
            return s
        except ValueError:
            return 0
    

    def csv_read(self):
        with open('Thurs12-3Log.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter = ',')
            counter = 0
            speedcolm = 13
            rpmcolm = 12
            throttlecolm = 14
            distcolm = 15
            mpgcolm = 16
            timecolm = 0
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
            self.text = Text(self, height = 11, width = 40)
            self.text.grid()
            message1 = "\nYour trip began at this time: " + str(tripdate)
            self.text.insert(1.0, message1)
            message2 = "\nOn this trip you traveled " + str(totaldist) + " miles in " + str(totalmin) + " minutes"
            self.text.insert(END, message2)
            message3 = "\nMax speed for this trip was " + str(maxspd) + " mph"
            self.text.insert(END, message3)
            if maxspd > 65:
                message4 = "\n- **You're speeding!**"
            else:
                message4 = ""
            self.text.insert(END, message4)
            message5 = "\nMax engine RPM for this trip was " + str(maxrmp)
            self.text.insert(END, message5)
            message6 = "\nMax throttle position for this trip was " + str(maxthrottle) + " %"
            self.text.insert(END, message6)
            if maxthrottle > 70:
                message7 = "\nYou're flooring it!"
                self.text.insert(END, message7)
            message8 = "\nYour average miles per gallon was " + str(avgmpg)
            self.text.insert(END, message8)


root = Tk()
root.title("OBD2 GUI")
root.geometry("400x300")
app = OBD2(root)
root.mainloop()
