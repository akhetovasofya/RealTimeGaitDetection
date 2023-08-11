#Written by Sofya Akhetova
import pandas as pd
import os
import csv
import numpy as np
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import queue
import global_variables

def finding_IC(values):
    falling = False #Whether we started to fall
    for i in range(2, len(values)):
        if values[i]-values[i-1]<-10:
            falling = True
        if values[i]-values[i-1]>0 and values[i-1]-values[i-2]<0 and values[i]<0 and values[i-1]<0 and values[i-2]<0 and falling:
            return i-1

directory = global_variables.directory
directory_for_saving = global_variables.directory_detected
directory_for_saving_file_truth = global_variables.directory_file_truth
for filename in os.listdir(directory):
    
    if filename.endswith(".csv"):
        name = filename.split('.csv')[0]
        name_split = name.split("_")
        if name_split[-1]=="truth":
            continue
        with open(os.path.join(directory, filename), "r") as file:
            # Create a CSV reader
            imu = csv.reader(file)
            
            # Skip the header row
            next(imu)
            
            #Doing only this file
            #if filename!="GRT05_slow_31.csv":
            #    continue

            #Skipping some files
            if name_split[0] == "GRT03":
                continue

            #The imu was flipped for the right foot, so we flip it in post processing
            right_foot = 1
            if name_split[0] == "GRT07" or name_split[0] == "GRT09" or name_split[0] == "GRT05" or name_split[0] =="sofya" or  name_split[0] =="GRT02":
                right_foot=-1
            if name_split[0] == "GRT03" and name_split[-2]=="right":
                right_foot=-1

            #To know in the log which file we are on
            print(filename)
            

            #All recorded values
            peaks_value = [] #max peak
            peaks_time = [] #max peak
            detectedTO_value = [] #TO that is our algo's decision
            detectedIC_value = [] #IC that is our algo's decision
            shouldveTO_value = [] #TO where it should've been
            shouldveIC_value = [] #IC where it should've been
            detectedTO_time = [] #TO that is our algo's decision
            detectedIC_time = [] #IC that is our algo's decision
            shouldveTO_time = [] #TO where it should've been
            shouldveIC_time = [] #IC where it should've been
            TOdelay = [] #delay of TO (detectedTO-shouldveTO)
            ICdelay = [] #delay of IC (detectedIC-shouldveIC)
            all_step_time = [] #Records how long each step is
            standing_time = [] #Records how long standing time is (shouldveTO-shouldveIC)

            #Ratio numbers
            peaks_ratio = 0.7 #for thresholds
            step_time_ratio = 0.6 #to not error out on noise

            #How many last steps to use
            steps = 3

            #A peak threshold to detect the first calibration step
            average_peak = 100
            average_time = 1000 #in ms

            #setting previous
            prev_point = 0
            prev_time = 0
            second_prev_point = 0
            second_prev_time = 0

            #A place to record current step untill we analyze it
            step_values = []
            step_time = []

            #State Machine Terms
            first_peak = False
            

            # Iterate through each row of data
            for index, row in enumerate(imu):

                #Skipping if line is too short which happens at the end
                if not row[9]:
                    continue
                
                #Getting time and point values
                current_point = float(row[6])*right_foot
                current_time = float(row[9])

                
####################################################################################
                #Starting Real-Time Analysis
####################################################################################

                #Seeing if current_point is bigger then peaks
                #We do a range of steps because if takes time to get to step amount
                #This will get the rolling average of the last 3 items or less if there are no 3 items
                for i in range(1,steps):
                    if len(peaks_value)>=i:
                        average_peak = sum(peaks_value[len(peaks_value)-i:])/i
                        average_time = sum(all_step_time[len(all_step_time)-i:])/i

                if current_point>average_peak*peaks_ratio:
                    
                    #Incase it is too short due to noise
                    if step_time_ratio*average_time < (current_time-step_time[0]) and not first_peak:
                        #Recording some values
                        peaks_value.append(max(step_values)) #finding the max
                        peaks_time.append(step_time[step_values.index(max(step_values))]) #finding the index to the max to match it's timing
                        #print("time step: ", step_time)
                        #print("time values: ", step_values)

                        #the logic of finding where TO and IC should've been is through getting local minimums and taking the first one for IC and last one for TO
                        #the logic for first minimum to be IC is because that should be the initial change thus would be the first drastic minimum. After that, there is probably a bit of noise.
                        #The logic for the last minimum for TO is because once toes are lifted it will become positive so the most reliable minimum is probably going to be the last one
                        local_mins_index = argrelextrema(np.array(step_values), np.less)[0]
                        IC_index = finding_IC(step_values)
                        shouldveTO_value.append(step_values[local_mins_index[-1]]) #TO where it should've been
                        shouldveIC_value.append(step_values[IC_index]) #IC where it should've been
                        shouldveTO_time.append(step_time[local_mins_index[-1]]) #TO where it should've been
                        shouldveIC_time.append(step_time[IC_index]) #IC where it should've been
                        #TOdelay.append(detectedTO[-1]-shouldveTO[-1])
                        #ICdelay.append(detectedIC[-1]-shouldveIC[-1])
                        all_step_time.append(step_time[-1]-step_time[0])
                        #standing_time.append(shouldveIC[-1]-shouldveTO[-1])

                        #Clearing the last step
                        step_values.clear()
                        step_time.clear()

                    #Only do it once
                    first_peak = True
                else:
                    first_peak = False
                
                step_values.append(current_point)
                step_time.append(current_time)



                #Recodring Previous Values
                second_prev_point = prev_point
                second_prev_time = prev_time
                prev_point = current_point
                prev_time = current_time
                


                        

####################################################################################
                #Printing For Terminal
####################################################################################

        #Printing the list of all values, mostly for debugging sake
        print()
        print("POINTS:")
        print("peaks value: ", peaks_value)
        print("peaks time: ", peaks_time)
        print("detectedTO value: ", detectedTO_value)
        print("detectedTO time: ", detectedTO_time)
        print("detectedIC value: ", detectedIC_value)
        print("detectedIC time: ", detectedIC_time)
        print("shouldveTO value: ", shouldveTO_value)
        print("shouldveTO time: ", shouldveTO_time)
        print("shouldveIC value: ", shouldveIC_value)
        print("shouldveIC time: ", shouldveIC_time)
        print()
        print("DELAYS:")
        print("ICdelay: ",ICdelay)
        print("TOdelay: ", TOdelay)
        print()
        print("TIMINGS:")
        print("step_time: ",step_time)
        print("standing_time: ", standing_time)
        print()

####################################################################################
                #Recording data
####################################################################################

        # Open a new CSV file for writing
        with open((os.path.join(directory_for_saving, name + "_detected.csv")), "w", newline="") as csvfile:
            #Opening writing file
            writer = csv.writer(csvfile)

            #Creating titles
            writer.writerow(["Peaks Value","Peaks Time","IC Detected Value","IC Detected Time","TO Detected Value", "TO Detected Time", "Where IC Should've Been Value","Where IC Should've Been Time","Where TO Should've Been Value","Where TO Should've Been Time", "IC Delay", "TO Delay"])
            
            #Finding the longest list
            longestTime = [len(peaks_value),len(peaks_time), len(detectedIC_value),len(detectedIC_time), len(detectedTO_value),len(detectedTO_time), len(shouldveIC_value), len(shouldveIC_time),len(shouldveTO_value), len(shouldveTO_time), len(ICdelay), len(TOdelay)]
            for i in range(0,max(longestTime)):
                
                #Recodring all the values into their own columns
                printing_list = ["","","","","","","", "", "", "", "", ""]
                if i<len(peaks_value):
                    printing_list[0] = peaks_value[i]
                if i<len(peaks_time):
                    printing_list[1] = peaks_time[i]
                if i<len(detectedIC_value):
                    printing_list[2] = detectedIC_value[i]
                if i<len(detectedIC_time):
                    printing_list[3] = detectedIC_time[i]
                if i <len(detectedTO_value):
                    printing_list[4] = detectedTO_value[i]
                if i <len(detectedTO_time):
                    printing_list[5] = detectedTO_time[i]
                if i <len(shouldveIC_value):
                    printing_list[6] = shouldveIC_value[i]
                if i <len(shouldveIC_time):
                    printing_list[7] = shouldveIC_time[i]
                if i<len(shouldveTO_value):
                    printing_list[8] = shouldveTO_value[i]
                if i<len(shouldveTO_time):
                    printing_list[9] = shouldveTO_time[i]
                if i <len(ICdelay):
                    printing_list[10] = ICdelay[i]
                if i <len(TOdelay):
                    printing_list[11] = TOdelay[i]
                writer.writerow(printing_list)

        #break

