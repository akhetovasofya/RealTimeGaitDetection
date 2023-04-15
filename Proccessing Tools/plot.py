import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import csv
# Set the directory path to search for .log files
directory = "C:/Users/aheto/Documents/research/recording FSR big 10 people study/RealTimeGaitDetection\DataProccessing"
for filename in os.listdir(directory):
    # Check if the file is a .log file
    if filename.endswith(".csv"):
        name = substrings = filename.split('_')
        if name[1] == "med":
            name[1] = "Medium"
        name = name[0].capitalize() + " " + name[1].capitalize()

        plt.figure(figsize=(20, 5))
        plt.rcParams.update({'font.size': 20})
        imu = pd.read_csv(os.path.join(directory, filename))

        plt.plot(imu[imu.columns[9]], imu[imu.columns[6]]*-1, label="Angular Velocity\n in Z (deg/s)", linewidth=1.0, zorder=-1)
        plt.plot(imu[imu.columns[9]], imu[imu.columns[7]], label="FSR Toe", linewidth=1.0, zorder=-1)
        plt.plot(imu[imu.columns[9]], imu[imu.columns[8]], label="FSR Heel", linewidth=1.0, zorder=-1)

        #getting IC and TO from data
        
        ICtime = []
        TOtime =[]

        #detect fast changes in velocity for toes off
        threshold_TO = -10
        prev_time_index = 0
        for i in range(1, len(imu[imu.columns[7]])):
            diff = imu[imu.columns[7]][i] - imu[imu.columns[7]][i-1]
            if diff < threshold_TO:
                TOtime.append(imu[imu.columns[9]][i])
                if (imu[imu.columns[9]][i]-imu[imu.columns[9]][prev_time_index]) <300:
                    del TOtime[-2]
                prev_time_index = i

        #detect fast changes in velocity for initial contact
        threshold_IC = 10
        prev_time_index = 0
        for i in range(1, len(imu[imu.columns[8]])):
            diff = imu[imu.columns[8]][i] - imu[imu.columns[8]][i-1]
            if diff > threshold_IC:
                if (imu[imu.columns[9]][i]-imu[imu.columns[9]][prev_time_index]) <300:
                    continue
                ICtime.append(imu[imu.columns[9]][i])
                prev_time_index = i


        IC = [0]*len(ICtime)
        TO = [0]*len(TOtime)
        plt.scatter(ICtime, IC, label="IC", color='red', linewidth=1.0, zorder=1)
        plt.scatter(TOtime, TO, label="TO", color='purple', linewidth=1.0, zorder=1)

        # Add labels and legend
        plt.xlabel("Time (ms)")
        plt.title(name)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))


        # Show the plot
        plt.show()






