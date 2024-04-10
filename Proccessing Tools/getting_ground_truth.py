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

    
    if filename.endswith(".csv"):
        name = filename.split('.csv')[0]
        name_sections = filename.split('_')
        print(filename)
        #skipping the done sections
        imu = pd.read_csv(os.path.join(directory, filename))

        #getting IC and TO from data
        
        ICtime = []
        TOtime =[]


        time_protection = 500
        #detect fast changes in velocity for toes off
        threshold_TO = -7
        prev_time_index = 0
        for i in range(3, len(imu[imu.columns[7]])):
            diff = imu[imu.columns[7]][i-1] -imu[imu.columns[7]][i]
            if diff == imu[imu.columns[7]][i-1] and diff!=0 and (imu[imu.columns[7]][i-2]>3 or imu[imu.columns[7]][i-3]>3):
                TOtime.append(imu[imu.columns[9]][i])
                if prev_time_index!=0 and (imu[imu.columns[9]][i]-imu[imu.columns[9]][prev_time_index]) <time_protection/2:
                    del TOtime[-2]
                prev_time_index = i

        #detect fast changes in velocity for initial contact
        threshold_IC = 7
        prev_time_index = 0
        for i in range(3, len(imu[imu.columns[8]])):
            diff = imu[imu.columns[8]][i-2] - imu[imu.columns[8]][i-3]
            if diff == imu[imu.columns[8]][i-2] and (imu[imu.columns[8]][i-1]>3 or imu[imu.columns[8]][i]>3) and diff!=0:
                #if prev_time_index!=0 and (imu[imu.columns[9]][i-1]-imu[imu.columns[9]][prev_time_index]) <time_protection :
                #    continue
                #if (i-1)<len(TOtime) and i>=1 and (abs(TOtime[i]- imu[imu.columns[9]][i-1])<200 or abs(TOtime[i-1]- imu[imu.columns[9]][i-1])<200 or abs(TOtime[i+1]- imu[imu.columns[9]][i-1])<200 ):
                #    continue
                if (len(ICtime)>=1 and 1000*.7<=(imu[imu.columns[9]][i-3]-ICtime[-1])) or len(ICtime)<1:
                    ICtime.append(imu[imu.columns[9]][i-3])
                prev_time_index = i
            
    
    
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







