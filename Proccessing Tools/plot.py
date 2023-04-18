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

        #if filename.split('_')[0] == "becca":
            #continue

        right_foot = 1
        if name[0] == "becca" or name[0] == "ryan" or name[0] == "patrick" or name[0] =="sofya" or  name[0] =="josh":
            right_foot=-1
        if name[0] == "madeleine" and name[-2]=="right":
            right_foot=-1
        pretty_name = name[0].capitalize() + " " + name[1].capitalize()
        name = filename.split('.csv')[0]

        plt.figure(figsize=(20, 5))
        plt.rcParams.update({'font.size': 20})

        imu = pd.read_csv(os.path.join(directory, filename))
        

        plt.plot(imu[imu.columns[9]], imu[imu.columns[6]]*right_foot, label="Angular Velocity\n in Z (deg/s)", linewidth=1.0, zorder=-1)
        plt.plot(imu[imu.columns[9]], imu[imu.columns[7]], label="FSR Toe", linewidth=1.0, zorder=-1)
        plt.plot(imu[imu.columns[9]], imu[imu.columns[8]], label="FSR Heel", linewidth=1.0, zorder=-1)

        
        ground_truth = pd.read_csv(os.path.join(directory_ground_truth, filename.split('.csv')[0]+ "_ground_truth.csv"))
        #ground truth
        TOtime_old = ground_truth[ground_truth.columns[0]]
        TOtime_old = TOtime_old.values.tolist()
        ICtime_old = ground_truth[ground_truth.columns[1]]
        ICtime_old = ICtime_old.values.tolist()


        #########   DOTS FOR WHAT IT'S SUPPOSED TO BE  #####################

        #detected
        detected = pd.read_csv(os.path.join(directory_detected, filename.split('.csv')[0]+ "_detected.csv"))
        TOs_old = detected[detected.columns[0]]
        TOs_old = TOs_old.values.tolist()
        TOg_old = detected[detected.columns[1]]
        TOg_old = TOg_old.values.tolist()
        ICs_old = detected[detected.columns[2]]
        ICs_old = ICs_old.values.tolist()
        ICg_old = detected[detected.columns[3]]
        ICg_old = ICg_old.values.tolist()

        
        
        
        
        #deleting unused
        TOtime = []
        ICtime = []
        ICs = []
        ICg = []
        TOs = []
        TOg = []
        for i in range(0, len(TOs_old)):
            if TOs_old[i] == TOs_old[i]:
                TOs.append(TOs_old[i]) # deleting NaNs
                TOg.append(TOg_old[i]) # deleting NaNs
        for i in range(0, len(ICs_old)):
            if ICs_old[i] == ICs_old[i]:
                ICs.append(ICs_old[i]) # deleting NaNs
                ICg.append(ICg_old[i]) # deleting NaNs
        for i in range(0, len(TOtime)):
            if TOtime[i] != TOtime[i]:
                del TOtime[i] # deleting NaNs
        for i in range(0, len(ICtime)):
            if ICtime[i] != ICtime[i]:
                del ICtime[i] # deleting NaNs

        if len(TOs) == 0 or len(ICs) == 0:
            print("ERRROR IN DETECTED")
            continue
        

        ##################################################
        ########removing before and after detected
        if ICs[0]>TOs[0]:
            first_detected = TOs[0]-200
        else:
            first_detected = ICs[0]-200
        
        if ICs[-1]>TOs[-1]:
            last_detected = ICs[-1]+200
        else:
            last_detected = TOs[-1]+200


        for ic_index in ICtime_old:
            if ic_index>first_detected and ic_index<last_detected:
                ICtime.append(ic_index)
        for to_index in TOtime_old:
            if to_index>first_detected and to_index<last_detected:
                TOtime.append(to_index)
        
        ########################################################
        ########################################################

        IC = [0]*len(ICtime)
        TO = [0]*len(TOtime)
        #TO
        plt.scatter(TOtime, TO, marker='o',s=10, label="TO from FSR", facecolors='none', edgecolors='purple', linewidth=1.0, zorder=1)
        #IC
        plt.scatter(ICtime, IC, marker='o',s=10, label="IC from FSR", facecolors='none', edgecolors='red',linewidth=1.0, zorder=1)
        

        plt.scatter(ICs, ICg, label="IC detected", color='red', linewidth=1.0, zorder=1)
        plt.scatter(TOs, TOg, label="TO detected", color='purple', linewidth=1.0, zorder=1)

        


        # Add labels and legend
        plt.xlabel("Time (ms)")
        plt.title(pretty_name)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

        
        # Show the plot
        plt.show()
        #plt.savefig(os.path.join(directory_of_graphs, name + ".png"))


        





