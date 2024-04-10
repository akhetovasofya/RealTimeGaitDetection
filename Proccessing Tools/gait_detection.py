#Written by Sofya Akhetova
import pandas as pd
import os
import csv
import numpy as np
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import queue
import global_variables

#This function will give you the index of the IC event when you give it a whole step
#It does it through the logic of first detecting a significant negative slope. When we have that, we know that we are "falling" from the peak.
#Then the first moment we stop falling and are in the negatives, we reached the "stoppped falling".
def finding_IC(values):
    was_positive = False
    falling = False #Whether we started to fall
    for i in range(3, len(values)):
        #values[i-1]-values[i-2]>0 is when I expect the turn from neg to pos but I want to make sure that the slopes before is neg enough, and slope after is pos enough
        #current point is i-2
        if values[i]-values[i-1]>0 and values[i-1]-values[i-2]>0 and values[i-2]-values[i-3]<0 and values[i-1]<0 and values[i-2]<0 and values[i-3]<0 and falling and was_positive:
            return i-2
        if values[i]-values[i-1]<-5:
            falling = True
        if values[i]>0:
            was_positive = True
    print("Error: Couldn't find should've IC")
    return -1


#This function will give you the index of the IC event when you give it a whole step
#The logic of it is to record the lowest point right where it just had a negative slope and now the next point has a positive slope
def finding_TO(values):
    fall_down_from_peak = False
    TOindex = -1
    TOvalue = 0
    for i in range(round(len(values)*0.5)+2, len(values)):
        #current point is i-1
        if values[i-1]-values[i-2]<= 0 and values[i]-values[i-1]>=0 and values[i-1]<TOvalue and values[i-1]<0:
            TOvalue = values[i-1]
            TOindex = i-1
            fall_down_from_peak = True
        if values[i]>0 and fall_down_from_peak:
            return TOindex
    print("Error: Couldn't find should've TO")
    return TOindex


#Getting directories of all the files
directory = global_variables.directory
directory_for_saving = global_variables.directory_detected
directory_for_saving_file_truth = global_variables.directory_file_truth

#opening the directories
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
           # if filename!="GRT04_slow_31.csv":
                #continue

            #Skipping some files
            if name_split[0] == "GRT03" or name[0] == "GRT08":
                continue

            #The imu was flipped for the right foot, so we flip it in post processing
            right_foot = 1
            if name_split[0] == "GRT07" or name_split[0] == "GRT09" or name_split[0] == "GRT05" or  name_split[0] =="GRT02":
                right_foot=-1
            if name_split[0] == "GRT03" and name_split[-2]=="right":
                right_foot=-1

            #To know in the log which file we are on
            print(filename)
            

            #All recorded values
            peaks_value = [] #max peak
            peaks_time = [] #max peak
            initial_detectedTO_value = [] #TO that is initially detected
            initial_detectedIC_value = [] #IC that is initially detected
            final_detectedTO_value = [] #TO that algo detected
            final_detectedIC_value = [] #IC that algo detected
            shouldveTO_value = [] #TO where it should've been
            shouldveIC_value = [] #IC where it should've been
            initial_detectedTO_time = [] #TO that is initially detected
            initial_detectedIC_time = [] #IC that is initially detected
            final_detectedTO_time = [] #TO that algo detected
            final_detectedIC_time = [] #IC that algo detected
            shouldveTO_time = [] #TO where it should've been
            shouldveIC_time = [] #IC where it should've been
            TOdelay = [] #delay of TO (detectedTO-shouldveTO) but only positive
            ICdelay = [] #delay of IC (detectedIC-shouldveIC) but only positive
            all_step_time = [] #Records how long each step is
            standing_time = [] #Records how long standing time is (shouldveTO-shouldveIC)

            #Ratio numbers
            peaks_ratio = 0.7 #for thresholds
            step_time_ratio = 0.6 #to not error out on noise
            IC_ratio = 0.7
            TO_ratio = 0.7
            standing_time_ratio = 0.7
            precautionary_slop = 10

            #How many last strides to use
            strides = 3

            #A peak threshold to detect the first calibration step
            #giving initial values mostly for calibration
            average_peak = 100
            average_time = 1000 #in ms
            average_TO = -1
            average_IC = -1
            average_standing_time = 500 #in ms
            average_TOdelay = 0
            average_ICdelay = 0

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
            IChappened = False  
            TOhappened = False 
            initialIC = False
            initialTO = False         

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
                #We do a range of strides because if takes time to get to step amount
                #This will get the rolling average of the last 3 items or less if there are no 3 items
                for i in range(1,strides):
                    if len(peaks_value)>=i:
                        average_peak = sum(peaks_value[len(peaks_value)-i:])/i
                        average_time = sum(all_step_time[len(all_step_time)-i:])/i
                    if len(shouldveIC_value)>=i:
                        average_IC = sum(shouldveIC_value[len(shouldveIC_value)-i:])/i
                    if len(shouldveTO_value)>=i:
                        average_TO = sum(shouldveTO_value[len(shouldveTO_value)-i:])/i
                    if len(standing_time)>=i:
                        average_standing_time = sum(standing_time[len(standing_time)-i:])/i
                    if len(ICdelay)>=i:
                        average_ICdelay = sum(ICdelay[len(ICdelay)-i:])/i
                    if len(TOdelay)>=i:
                        average_TOdelay = sum(TOdelay[len(TOdelay)-i:])/i


                if current_point>average_peak*peaks_ratio:
                    
                    #Incase it is too short due to noise
                    if step_time_ratio*average_time < (current_time-step_time[0]) and not first_peak:
                        
                        #Resetting State Machine values
                        IChappened = False
                        TOhappened = False
                        initialIC = False
                        initialTO = False
                        
                        #Recording some values
                        peaks_value.append(max(step_values)) #finding the max
                        peaks_time.append(step_time[step_values.index(max(step_values))]) #finding the index to the max to match it's timing

                        local_mins_index = argrelextrema(np.array(step_values), np.less)[0]
                        IC_index = finding_IC(step_values) #function to find the local min of IC
                        TO_index = finding_TO(step_values) #function to find the local min of TO
                        shouldveTO_value.append(step_values[TO_index]) #TO where it should've been
                        shouldveIC_value.append(step_values[IC_index]) #IC where it should've been
                        shouldveTO_time.append(step_time[TO_index]) #TO where it should've been
                        shouldveIC_time.append(step_time[IC_index]) #IC where it should've been

                        #If TO and IC empty, that means it's their first step so we need to append the first should've value
                        if not initial_detectedTO_value:
                            initial_detectedTO_value.append(shouldveTO_value[-1])
                            initial_detectedTO_time.append(shouldveTO_time[-1])
                        if not initial_detectedIC_value:
                            initial_detectedIC_value.append(shouldveIC_value[-1])
                            initial_detectedIC_time.append(shouldveIC_time[-1])

                        #I only want to append if the delay is positive as that means detected happened before should've which means I can delay the event
                        #If it's negetive, it means that detected happened after should've thus I can't delay. If it's zero than it hit the safety.
                        if shouldveTO_time[-1]-initial_detectedTO_time[-1] > 0:
                            TOdelay.append(shouldveTO_time[-1]-initial_detectedTO_time[-1])
                        if shouldveIC_time[-1]-initial_detectedIC_time[-1] > 0:
                            ICdelay.append(shouldveIC_time[-1]-initial_detectedIC_time[-1])

                        all_step_time.append(step_time[-1]-step_time[0])
                        standing_time.append(shouldveTO_time[-1] - shouldveIC_time[-1])

                        #Clearing the last step
                        step_values.clear()
                        step_time.clear()

                    #Only do it once
                    first_peak = True

                # Left portion is checking whether calibrated, whether IC has not happened in the step, and whether this point is bellow our IC threshold
                # Right is a IC precaution that if the slope is very large, we call the event
                elif not IChappened and average_IC!=-1 and(( current_point < IC_ratio*average_IC) or ((current_point-prev_point)>precautionary_slop) and current_point<0):

                    #safety conditions has been triggered
                    if (current_point-prev_point)>precautionary_slop:
                        if not initialIC:
                            initialIC = True
                            initial_detectedIC_value.append(current_point)
                            initial_detectedIC_time.append(current_time)
                        if not IChappened:
                            IChappened = True
                            final_detectedIC_value.append(current_point)
                            final_detectedIC_time.append(current_time)

                    #detecteding the first 
                    elif not initialIC:
                        initialIC = True
                        initial_detectedIC_value.append(current_point)
                        initial_detectedIC_time.append(current_time)

                    elif not IChappened and initialIC and (current_time-initial_detectedIC_time[-1])>=average_ICdelay:
                        IChappened = True
                        final_detectedIC_value.append(current_point)
                        final_detectedIC_time.append(current_time)

                #Left portion is checking whether calibrated, whether TO has not happend but IC did in the step, and whether the timing bigged than average standing time
                # Right is a TO precaution that if the slope is very large, we call the event
                elif not TOhappened and IChappened and (current_time-initial_detectedIC_time[-1])>average_standing_time*standing_time_ratio and average_TO!=-1 and ((current_point < TO_ratio*average_TO) or ((current_point-prev_point)>precautionary_slop and current_point<0)):
                    #take out last cur<0 TODO
                    
                    #Safety
                    if (current_point-prev_point)>precautionary_slop:
                        if not initialTO:
                            initialTO = True
                            initial_detectedTO_value.append(current_point)
                            initial_detectedTO_time.append(current_time)
                        if not TOhappened:
                            TOhappened = True
                            final_detectedTO_value.append(current_point)
                            final_detectedTO_time.append(current_time)

                    #detecteding the first 
                    elif not initialTO:
                        initialTO = True
                        initial_detectedTO_value.append(current_point)
                        initial_detectedTO_time.append(current_time)

                    #detecting final
                    elif not TOhappened and initialTO and (current_time-initial_detectedTO_time[-1])>=average_TOdelay:
                        TOhappened = True
                        final_detectedTO_value.append(current_point)
                        final_detectedTO_time.append(current_time)

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
        print("init detectedTO value: ", initial_detectedTO_value)
        print("init detectedTO time: ", initial_detectedTO_time)
        print("init detectedIC value: ", initial_detectedIC_value)
        print("init detectedIC time: ", initial_detectedIC_time)
        print("final detectedTO value: ", final_detectedTO_value)
        print("final detectedTO time: ", final_detectedTO_time)
        print("final detectedIC value: ", final_detectedIC_value)
        print("final detectedIC time: ", final_detectedIC_time)
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
            writer.writerow(["Peaks Value","Peaks Time","IC Detected Value","IC Detected Time","TO Detected Value", "TO Detected Time", "Where IC Should've Been Value","Where IC Should've Been Time","Where TO Should've Been Value","Where TO Should've Been Time", "IC Delay", "TO Delay", "Inital Detected IC value", "Initial Detected IC time", "Initial Detected TO value", "Initial Detected TO time", "Stance Time"])
            
            #Finding the longest list
            longestTime = [len(initial_detectedTO_time),len(initial_detectedIC_time),len(peaks_value),len(peaks_time), len(final_detectedIC_value),len(final_detectedIC_time), len(final_detectedTO_value),len(final_detectedTO_time), len(shouldveIC_value), len(shouldveIC_time),len(shouldveTO_value), len(shouldveTO_time), len(ICdelay), len(TOdelay), len(standing_time)]
            for i in range(0,max(longestTime)):
                
                #Recodring all the values into their own columns
                printing_list = ["","","","","","","", "", "", "", "", "","", "", "", "", ""]
                if i<len(peaks_value):
                    printing_list[0] = peaks_value[i]
                if i<len(peaks_time):
                    printing_list[1] = peaks_time[i]
                if i<len(final_detectedIC_value):
                    printing_list[2] = final_detectedIC_value[i]
                if i<len(final_detectedIC_time):
                    printing_list[3] = final_detectedIC_time[i]
                if i <len(final_detectedTO_value):
                    printing_list[4] = final_detectedTO_value[i]
                if i <len(final_detectedTO_time):
                    printing_list[5] = final_detectedTO_time[i]
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
                if i <len(initial_detectedIC_value):
                    printing_list[12] = initial_detectedIC_value[i]
                if i <len(initial_detectedIC_time):
                    printing_list[13] = initial_detectedIC_time[i]
                if i <len(initial_detectedTO_value):
                    printing_list[14] = initial_detectedTO_value[i]
                if i <len(initial_detectedTO_time):
                    printing_list[15] = initial_detectedTO_time[i]
                if i<len(standing_time):
                    printing_list[16] = standing_time[i]
                writer.writerow(printing_list)

        #break

