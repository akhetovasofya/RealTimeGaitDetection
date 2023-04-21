#Thoughts:
# 1. put calibration protection to make sure calibration step was good




import pandas as pd
import os
import csv

import matplotlib.pyplot as plt
import queue

import global_variables
directory = global_variables.directory
directory_for_saving = global_variables.directory_detected
for filename in os.listdir(directory):
    
    if filename.endswith(".csv"):
        name = filename.split('.csv')[0]
        name_split = name.split("_")
        if name_split[-1]=="truth":
            continue
        print()
        print(filename)
        #if name_split[0]!="becca":
            #continue
        with open(os.path.join(directory, filename), "r") as file:
            # Create a CSV reader
            imu = csv.reader(file)
            print()
            print()
            print(filename)
            # Skip the header row
            next(imu)
            next(imu)
            if name_split[0] == "GRT03":
                continue
            right_foot = 1
            if name_split[0] == "GRT07" or name_split[0] == "GRT09" or name_split[0] == "GRT05" or name_split[0] =="sofya" or  name_split[0] =="GRT02":
                right_foot=-1
            if name_split[0] == "GRT03" and name_split[-2]=="right":
                right_foot=-1

            TOs = []
            ICs = []

            #for graphing
            TOg = []
            ICg = []
            peaktime = []
            peakvalue = []
            peak_threshold = 150
            low_threshold = -100
            reached_peak = 0
            reached_IC = 0
            reached_TO = 0


            # Iterate through each row
            for index, row in enumerate(imu):
                # Access individual values by index
                #print(row[9], row[6])

                if index <200:
                    continue

                if len(row)<9:
                    continue

                current_point = float(row[6])*right_foot
                #print(row)
                current_time = float(row[9])

                if (True):
                    
                    #peak
                    
                    if current_point>peak_threshold and not reached_peak:
                        reached_peak = 1
                        peakvalue.append(current_point)
                        peaktime.append(current_time)
                    elif reached_peak and current_point<low_threshold and not reached_IC:
                        reached_peak = 0
                        reached_IC = 1
                        ICs.append(current_time)
                        ICg.append(current_point)
                    elif reached_IC and current_point<low_threshold and not reached_TO:
                        if (current_time-ICs[-1])>80:
                            reached_IC = 0
                            reached_TO = 0
                            TOs.append(current_time)
                            TOg.append(current_point)




        print("peaktime:", peaktime)
        print("peakvalue:", peakvalue)
        print()
        print("ICs:", ICs)
        print("ICg:", ICg)
        print()
        print("TOs:", TOs)
        print("TOg:", TOg)
        print()
        # Open a new CSV file for writing
        with open((os.path.join(directory_for_saving, name + "_hard_thresh_detected.csv")), "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["TO time","TO value", "IC time", "IC value"])
            #if TO is longer than IC
            TOs = TOs[0:-1]
            ICs = ICs[0:-1]
            TOg = TOg[0:-1]
            ICg = ICg[0:-1]
            if len(TOs)>=len(ICs):
                for i in range(0,len(TOs)):
                    if i >=len(ICs):
                        writer.writerow([TOs[i], TOg[i], "", ""])
                    else:
                        writer.writerow([TOs[i], TOg[i], ICs[i], ICg[i]])
            else:
                for i in range(0,len(ICs)):
                    if i >=len(TOs):
                        writer.writerow(["","", ICs[i], ICg[i]])
                    else:
                        writer.writerow([TOs[i], TOg[i], ICs[i], ICg[i]])

