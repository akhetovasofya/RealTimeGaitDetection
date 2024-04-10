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
        if name[0] == "GRT03" or (name[0] == "GRT08" and name[1] == "vary") :
            continue
        
        #only analysing some files
        #if name[0] != "GRT10":
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
        fig, ax1 = plt.subplots() 
        ax1.plot(imu[imu.columns[9]], imu[imu.columns[6]]*right_foot, label="Angular Velocity\n in Z (deg/s)", linewidth=1.0, zorder=-1)
        ax2 = ax1.twinx() 
        ax2.plot(imu[imu.columns[9]], imu[imu.columns[7]]*3.3/1024, label="FSR Toe (V)", color='green', linewidth=1.0, zorder=-1)
        ax2.plot(imu[imu.columns[9]], imu[imu.columns[8]]*3.3/1024, label="FSR Heel (V)",color='orange',  linewidth=1.0, zorder=-1)

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

        #Detected TO and IC
        IC_value_detected = detected[detected.columns[2]]
        IC_value_detected = IC_value_detected.values.tolist()
        IC_time_detected = detected[detected.columns[3]]
        IC_time_detected = IC_time_detected.values.tolist()
        TO_value_detected = detected[detected.columns[4]]
        TO_value_detected = TO_value_detected.values.tolist()
        TO_time_detected = detected[detected.columns[5]]
        TO_time_detected = TO_time_detected.values.tolist()
        

        #Should've TO and IC
        shoulve_IC_value_detected = detected[detected.columns[6]]
        shoulve_IC_value_detected = shoulve_IC_value_detected.values.tolist()
        shoulve_IC_time_detected = detected[detected.columns[7]]
        shoulve_IC_time_detected = shoulve_IC_time_detected.values.tolist()
        shoulve_TO_value_detected = detected[detected.columns[8]]
        shoulve_TO_value_detected = shoulve_TO_value_detected.values.tolist()
        shoulve_TO_time_detected = detected[detected.columns[9]]
        shoulve_TO_time_detected = shoulve_TO_time_detected.values.tolist()

        #Initially Detected TO and IC
        init_IC_value_detected = detected[detected.columns[12]]
        init_IC_value_detected = init_IC_value_detected.values.tolist()
        init_IC_time_detected = detected[detected.columns[13]]
        init_IC_time_detected = init_IC_time_detected.values.tolist()
        init_TO_value_detected = detected[detected.columns[14]]
        init_TO_value_detected = init_TO_value_detected.values.tolist()
        init_TO_time_detected = detected[detected.columns[15]]
        init_TO_time_detected = init_TO_time_detected.values.tolist()

        #deleting unused
        checked_TO_GroundTruth = []
        checked_IC_GroundTruth = []
        checked_peaks_values_detected = []
        checked_peaks_time_detected = []
        checked_IC_value_detected = []
        checked_IC_time_detected = []
        checked_TO_value_detected = []
        checked_TO_time_detected = []
        checked_shoulve_IC_value_detected = []
        checked_shoulve_IC_time_detected = []
        checked_shoulve_TO_value_detected = []
        checked_shoulve_TO_time_detected = []
        checked_init_IC_value_detected = []
        checked_init_IC_time_detected = []
        checked_init_TO_value_detected = []
        checked_init_TO_time_detected = []

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
        
        #checking for detected IC
        for i in range(0, len(IC_value_detected)):
            if IC_value_detected[i] == IC_value_detected[i]:
                checked_IC_value_detected.append(IC_value_detected[i]) # deleting NaNs
        for i in range(0, len(IC_time_detected)):
            if IC_time_detected[i] == IC_time_detected[i]:
                checked_IC_time_detected.append(IC_time_detected[i]) # deleting NaNs
        
        #checking for detected TO
        for i in range(0, len(TO_value_detected)):
            if TO_value_detected[i] == TO_value_detected[i]:
                checked_TO_value_detected.append(TO_value_detected[i]) # deleting NaNs
        for i in range(0, len(TO_time_detected)):
            if TO_time_detected[i] == TO_time_detected[i]:
                checked_TO_time_detected.append(TO_time_detected[i]) # deleting NaNs

        #checking for should've IC
        for i in range(0, len(shoulve_IC_value_detected)):
            if shoulve_IC_value_detected[i] == shoulve_IC_value_detected[i]:
                checked_shoulve_IC_value_detected.append(shoulve_IC_value_detected[i]) # deleting NaNs
        for i in range(0, len(shoulve_IC_time_detected)):
            if shoulve_IC_time_detected[i] == shoulve_IC_time_detected[i]:
                checked_shoulve_IC_time_detected.append(shoulve_IC_time_detected[i]) # deleting NaNs
        
        #checking for should've TO
        for i in range(0, len(shoulve_TO_value_detected)):
            if shoulve_TO_value_detected[i] == shoulve_TO_value_detected[i]:
                checked_shoulve_TO_value_detected.append(shoulve_TO_value_detected[i]) # deleting NaNs
        for i in range(0, len(shoulve_TO_time_detected)):
            if shoulve_TO_time_detected[i] == shoulve_TO_time_detected[i]:
                checked_shoulve_TO_time_detected.append(shoulve_TO_time_detected[i]) # deleting NaNs

        #checking for initally detected IC
        for i in range(0, len(init_IC_value_detected)):
            if init_IC_value_detected[i] == init_IC_value_detected[i]:
                checked_init_IC_value_detected.append(init_IC_value_detected[i]) # deleting NaNs
        for i in range(0, len(init_IC_time_detected)):
            if init_IC_time_detected[i] == init_IC_time_detected[i]:
                checked_init_IC_time_detected.append(init_IC_time_detected[i]) # deleting NaNs
        
        #checking for initally detected TO
        for i in range(0, len(init_TO_value_detected)):
            if init_TO_value_detected[i] == init_TO_value_detected[i]:
                checked_init_TO_value_detected.append(init_TO_value_detected[i]) # deleting NaNs
        for i in range(0, len(init_TO_time_detected)):
            if init_TO_time_detected[i] == init_TO_time_detected[i]:
                checked_init_TO_time_detected.append(init_TO_time_detected[i]) # deleting NaNs

        
        if len(checked_peaks_values_detected)==0|len(checked_peaks_time_detected)==0|len(checked_shoulve_IC_value_detected)==0|len(checked_shoulve_IC_time_detected)==0|len(checked_shoulve_TO_value_detected)==0|len(checked_shoulve_TO_time_detected)==0:
            print("ERRROR IN DETECTED")
            continue
        
        #Ground Truth Plotting
        IC_GroundTruth_plotting = [10*3.3/1023]*len(checked_IC_GroundTruth)
        TO_GroundTruth_plotting = [10*3.3/1023]*len(checked_TO_GroundTruth)
        #TO
        ax2.scatter(checked_TO_GroundTruth, TO_GroundTruth_plotting, marker='o',s=20, label="FSR TO", facecolors='none', edgecolors='purple', linewidth=2.0, zorder=1)
        #IC
        ax2.scatter(checked_IC_GroundTruth, IC_GroundTruth_plotting, marker='o',s=20, label="FSR IC", facecolors='none', edgecolors='red',linewidth=2.0, zorder=1)
        
        #Detected
        ax1.scatter(checked_peaks_time_detected, checked_peaks_values_detected, facecolors='none', s=10, label="Threshold Mid-Swing", color='green', linewidth=1.5, zorder=1)
        ax1.scatter(checked_peaks_time_detected, checked_peaks_values_detected, s=10,label="Mid-Swing", color='green', linewidth=3, zorder=1)
        ax1.scatter(checked_shoulve_IC_time_detected, checked_shoulve_IC_value_detected, s=10,label="Ideal IC", color='red', linewidth=3, zorder=1)
        ax1.scatter(checked_shoulve_TO_time_detected, checked_shoulve_TO_value_detected, s=10,label="Ideal TO", color='blue', linewidth=3, zorder=1)
        ax1.scatter(checked_IC_time_detected, checked_IC_value_detected, s=10,label="Predicted IC", color='pink', linewidth=3, zorder=1)
        ax1.scatter(checked_TO_time_detected, checked_TO_value_detected, s=10,label="Predicted TO", color='cyan', linewidth=3, zorder=1)
        ax1.scatter(checked_init_IC_time_detected, checked_init_IC_value_detected, facecolors='none',s=15,label="Threshold IC", color='pink', linewidth=1.5, zorder=1)
        ax1.scatter(checked_init_TO_time_detected, checked_init_TO_value_detected, facecolors='none',s=15,label="Threshold TO", color='cyan', linewidth=1.5, zorder=1)


        # Add labels and legend
        ax2.set_ylabel("Measured Voltage (V)")
        ax2.set_ylim([-1, 1])
        ax1.set_xlabel("Time (ms)")
        ax1.set_ylabel("Angular Velocity (degrees/s)")
        plt.title(pretty_name)
        #plt.title("Imu Signal")
        #plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

        
        # Show the plot
        plt.show()
        #plt.savefig(os.path.join(directory_of_graphs, name + ".png"))

        #break


        





