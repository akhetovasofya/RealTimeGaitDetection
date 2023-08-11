import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import csv
import global_variables

# Set the directory path to search for .log files
directory = global_variables.directory
directory_ground_truth = global_variables.directory_ground_truth
directory_detected = global_variables.directory_detected
directory_of_graphs = global_variables.directory_of_graphs

#Opening all the files
for filename in os.listdir(directory):

    if filename.endswith(".csv"):

        #printing to see what was analysed/where errored
        print(filename)

        #formating all names
        name = filename.split('.csv')[0]
        name = name.split('_')

        if name[1] == "med":
            name[1] = "Medium"

        if name[1] == "vary":
            name[1] = "Varying Speeds"

        #skipping some files
        if name[0] == "GRT03" :
            continue
        
        #only analysing some files
        #if filename!="GRT05_slow_31.csv":
        #    continue

        #Flipping values for all the right legs as the imu was flipped
        right_foot = 1
        if name[0] == "GRT07" or name[0] == "GRT09" or name[0] == "GRT05" or name[0] =="sofya" or  name[0] =="GRT02":
            right_foot=-1
        if name[0] == "GRT03" and name[-2]=="right":
            right_foot=-1

        #Giving a pretty name
        pretty_name = "50m Walk"
        for i in range(0, len(name)-1):
            pretty_name +=" " + name[i]
        
        #Reading and plotting the imu and FSR data
        imu = pd.read_csv(os.path.join(directory, filename))
        plt.plot(imu[imu.columns[9]], imu[imu.columns[6]]*right_foot, label="Angular Velocity\n in Z (deg/s)", linewidth=1.0, zorder=-1)
        plt.plot(imu[imu.columns[9]], imu[imu.columns[7]], label="FSR Toe", linewidth=1.0, zorder=-1)
        plt.plot(imu[imu.columns[9]], imu[imu.columns[8]], label="FSR Heel", linewidth=1.0, zorder=-1)

        #Plotting the Ground Truth points
        ground_truth = pd.read_csv(os.path.join(directory_ground_truth, filename.split('.csv')[0]+ "_ground_truth.csv"))
        #ground truth
        TO_GroundTruth = ground_truth[ground_truth.columns[0]]
        TO_GroundTruth = TO_GroundTruth.values.tolist()
        IC_GroundTruth = ground_truth[ground_truth.columns[1]]
        IC_GroundTruth = IC_GroundTruth.values.tolist()


        #Plotting the Detected
        detected = pd.read_csv(os.path.join(directory_detected, filename.split('.csv')[0]+ "_detected.csv"))
        #Peaks
        peaks_value_detected = detected[detected.columns[0]]
        peaks_value_detected = peaks_value_detected.values.tolist()
        peaks_time_detected = detected[detected.columns[1]]
        peaks_time_detected = peaks_time_detected.values.tolist()
        
        #deleting unused
        checked_TO_GroundTruth = []
        checked_IC_GroundTruth = []
        checked_peaks_values_detected = []
        checked_peaks_time_detected = []

        #checking TO for Ground Truth
        for i in range(0, len(TO_GroundTruth)):
            if TO_GroundTruth[i] == TO_GroundTruth[i]:
                checked_TO_GroundTruth.append(TO_GroundTruth[i]) # deleting NaNs

        #checking IC for Ground Truth
        for i in range(0, len(IC_GroundTruth)):
            if IC_GroundTruth[i] == IC_GroundTruth[i]:
                checked_IC_GroundTruth.append(IC_GroundTruth[i]) # deleting NaNs
        
        #checking detected peaks
        for i in range(0, len(peaks_value_detected)):
            if peaks_value_detected[i] == peaks_value_detected[i]:
                checked_peaks_values_detected.append(peaks_value_detected[i]) # deleting NaNs
        for i in range(0, len(peaks_time_detected)):
            if peaks_time_detected[i] == peaks_time_detected[i]:
                checked_peaks_time_detected.append(peaks_time_detected[i]) # deleting NaNs
        
        if len(checked_peaks_values_detected) == 0 or len(checked_peaks_time_detected) == 0:
            print("ERRROR IN DETECTED")
            continue
        

        IC_GroundTruth_plotting = [0]*len(checked_IC_GroundTruth)
        TO_GroundTruth_plotting = [0]*len(checked_TO_GroundTruth)
        #TO
        plt.scatter(checked_TO_GroundTruth, TO_GroundTruth_plotting, marker='o',s=10, label="TO from FSR", facecolors='none', edgecolors='purple', linewidth=1.0, zorder=1)
        #IC
        plt.scatter(checked_IC_GroundTruth, IC_GroundTruth_plotting, marker='o',s=10, label="IC from FSR", facecolors='none', edgecolors='red',linewidth=1.0, zorder=1)
        


        plt.scatter(checked_peaks_time_detected, checked_peaks_values_detected, s=10,label="Peaks", color='green', linewidth=1.0, zorder=1)
        #plt.scatter(checked_peaks_time_detected, checked_peaks_values_detected, s=10,label="TO from IMU", color='pink', linewidth=1.0, zorder=1)
        #plt.scatter(ogICs, ogICg,s=10, label="IC from IMU", color='lightblue', linewidth=1.0, zorder=1)
        #plt.scatter(ICs, ICg,s=10, label="IC detected", color='red', linewidth=1.0, zorder=1)
        #plt.scatter(TOs, TOg,s=10, label="TO detected", color='blue', linewidth=1.0, zorder=1)

        


        # Add labels and legend
        plt.xlabel("Time (ms)")
        plt.title(pretty_name)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

        
        # Show the plot
        plt.show()
        #plt.savefig(os.path.join(directory_of_graphs, name + ".png"))

        #break


        





