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
for filename in os.listdir(directory):
    # Check if the file is a .log file
    #if filename.split('_')[0] != "tyler":
    #    continue

    if filename.endswith(".csv"):
        print(filename)
        name = filename.split('_')
        if name[1] == "med":
            name[1] = "Medium"

        if filename.split('_')[0] != "patrick":
            continue

        right_foot = 1
        if name[0] == "becca" or name[0] == "ryan" or name[0] == "patrick" or name[0] =="sofya" or  name[0] =="josh":
            right_foot=-1

        pretty_name = name[0].capitalize() + " " + name[1].capitalize()
        name = filename.split('.csv')[0]

        plt.figure(figsize=(20, 5))
        plt.rcParams.update({'font.size': 20})

        imu = pd.read_csv(os.path.join(directory, filename))
        

        plt.plot(imu[imu.columns[9]], imu[imu.columns[6]]*right_foot, label="Angular Velocity\n in Z (deg/s)", linewidth=1.0, zorder=-1)
        plt.plot(imu[imu.columns[9]], imu[imu.columns[7]], label="FSR Toe", linewidth=1.0, zorder=-1)
        plt.plot(imu[imu.columns[9]], imu[imu.columns[8]], label="FSR Heel", linewidth=1.0, zorder=-1)

        # Just Raw Data
        plt.xlabel("Time (ms)")
        plt.title(pretty_name)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        plt.show()
        continue
        ground_truth = pd.read_csv(os.path.join(directory_ground_truth, filename.split('.csv')[0]+ "_ground_truth.csv"))
        detected = pd.read_csv(os.path.join(directory_detected, filename.split('.csv')[0]+ "_detected.csv"))
        
        
        #########   DOTS FOR WHAT IT'S SUPPOSED TO BE  #####################

        #detected
        TOs = detected[detected.columns[0]]
        TOg = detected[detected.columns[1]]
        ICs = detected[detected.columns[2]]
        ICg = detected[detected.columns[3]]

        #ground truth
        TOtime = ground_truth[ground_truth.columns[0]]
        ICtime = ground_truth[ground_truth.columns[1]]
        
        
        
        #deleting unused
        for i in range(0, len(TOs)):
            if TOs[i] != TOs[i]:
                del TOs[i] # deleting NaNs
                del TOg[i] # deleting NaNs
        for i in range(0, len(ICs)):
            if ICs[i] != ICs[i]:
                del ICs[i] # deleting NaNs
                del ICg[i] # deleting NaNs

        if len(TOs) == 0 or len(ICs) == 0:
            print("ERRROR IN DETECTED")
            continue
        for i in range(0, len(TOtime)):
            if (TOs[0]-TOtime[i]) >200 or (TOtime[i] - TOs[len(TOs)-1])>200:
                del TOtime[i]
        for i in range(0, len(TOtime)):
            if (ICs[0]-ICtime[i])>200 or (ICtime[i] - ICs[len(ICs)-1])>200:
                del ICtime[i]

        IC = [0]*len(ICtime)
        TO = [0]*len(TOtime)

        plt.scatter(ICs, ICg, label="IC detected", color='red', linewidth=1.0, zorder=1)
        plt.scatter(TOs, TOg, label="TO detected", color='purple', linewidth=1.0, zorder=1)

        #TO
        plt.scatter(TOtime, TO, marker='o',s=10, label="TO from FSR", facecolors='none', edgecolors='purple', linewidth=1.0, zorder=1)
        #IC
        plt.scatter(ICtime, IC, marker='o',s=10, label="IC from FSR", facecolors='none', edgecolors='red',linewidth=1.0, zorder=1)


        # Add labels and legend
        plt.xlabel("Time (ms)")
        plt.title(pretty_name)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

        
        # Show the plot
        plt.show()
        #plt.savefig(os.path.join(directory_of_graphs, name + ".png"))


        





