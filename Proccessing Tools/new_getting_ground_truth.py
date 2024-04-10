import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import csv
# Set the directory path to search for .log files
import global_variables
directory = global_variables.directory
directory_for_saving = global_variables.directory_ground_truth
for filename in os.listdir(directory):
    # Check if the file is a .log file
    #if filename.split('_')[0]:
     #formating all names
    
    name = filename.split('.csv')[0]
    name = name.split('_')

    #skipping some files
    if name[0] == "GRT03" or (name[0] == "GRT08" and name[1] == "vary") :
        continue
        
    #only analysing some files
    #if filename!="GRT02_med_01.csv":
        #continue
    
    if filename.endswith(".csv"):
        name = filename.split('.csv')[0]
        name_sections = filename.split('_')
        print(filename)
        #skipping the done sections
        imu = pd.read_csv(os.path.join(directory, filename))

        #getting IC and TO from data
        
        ICtime = []
        TOtime =[]

        #Values to detect that it has done only once
        TO = False
        IC = True

        #Thresholds
        TO_thresh = 10
        IC_thresh = 10

        time_protection = 800
        TO_IC_time_protection = 300
        #detect fast changes in velocity for toes off
        
        #IC
        prev_time_index = 0
        for i in range(1, len(imu[imu.columns[8]])-1):
            if IC_thresh<imu[imu.columns[8]][i] and IC:
                if (imu[imu.columns[8]][i+1]-imu[imu.columns[8]][i-1]>0 and ((len(ICtime)!=0 and time_protection<imu[imu.columns[9]][i]-ICtime[-1]) or len(ICtime)==0)): # pos slope
                    ICtime.append(imu[imu.columns[9]][i])
                    IC = False
                    #print("IC false: ", imu[imu.columns[9]][i],  " ", imu[imu.columns[8]][i], " ", IC_thresh<imu[imu.columns[8]][i] )
            if IC_thresh>imu[imu.columns[8]][i] and not IC:
                IC = True
                #print("IC true: ", imu[imu.columns[9]][i],  " ", imu[imu.columns[8]][i], " ", IC_thresh>imu[imu.columns[8]][i])
        
        #TO
        prev_time_index = 0
        for i in range(1, len(imu[imu.columns[7]])-1):
            if TO_thresh<imu[imu.columns[7]][i]:
                TO = True
                #print("TO true: ", imu[imu.columns[9]][i], " ", imu[imu.columns[7]][i], " ", TO_thresh<imu[imu.columns[7]][i])
            if TO_thresh>imu[imu.columns[7]][i] and TO:
                 if (imu[imu.columns[7]][i+1]-imu[imu.columns[7]][i-1]<0 and ((len(TOtime)!=0 and time_protection<imu[imu.columns[9]][i]-TOtime[-1]) or len(TOtime)==0)): #neg slope
                    if (len(ICtime)==0 or (imu[imu.columns[9]][i]-ICtime[len(TOtime)])>TO_IC_time_protection):
                        TOtime.append(imu[imu.columns[9]][i])
                        TO = False
                        #print("TO false: ", imu[imu.columns[9]][i],  " ", imu[imu.columns[7]][i], " ", TO_thresh>imu[imu.columns[7]][i])
                        #if len(ICtime)!=0:
                            #print("IC to TO: ", (imu[imu.columns[9]][i]-ICtime[len(TOtime)-1]))
    
        # Open a new CSV file for writing
        with open((os.path.join(directory_for_saving, name + "_ground_truth.csv")), "w", newline="") as csvfile:
            print(name + "_ground_truth.csv")
            
            writer = csv.writer(csvfile)
            writer.writerow(["TO", "IC"])
            #if TO is longer than IC
            if len(TOtime)>=len(ICtime):
                #print(TOtime)
                for i in range(0,len(TOtime)):
                    if i >=len(ICtime):
                        writer.writerow([TOtime[i], ""])
                    else:
                        writer.writerow([TOtime[i], ICtime[i]])
            else:
                #print(ICtime)
                for i in range(0,len(ICtime)):
                    if i >=len(TOtime):
                        writer.writerow(["", ICtime[i]])
                    else:
                        writer.writerow([TOtime[i], ICtime[i]])







