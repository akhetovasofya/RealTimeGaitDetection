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
directory_final_calculations = global_variables.directory_final_calculations

with open((os.path.join(directory_final_calculations, "Final_Calculations.csv")), "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Which file:", "TO average delay", "IC average delay", "TO misses", "IC misses", "TO truth delay", "IC truth delay"])
    overallTOslow = []
    overallICslow = []
    overallTOmed = []
    overallICmed = []
    overallTOfast = []
    overallICfast = []
    overallTOvary = []
    overallICvary = []

    for filename in os.listdir(directory):
        # Check if the file is a .log file

        if filename.endswith(".csv"):
            name = filename.split('_')
            print(filename)
            print(filename)
            if name[0] == "GRT03":
                continue

            imu = pd.read_csv(os.path.join(directory, filename))
            ground_truth = pd.read_csv(os.path.join(directory_ground_truth, filename.split('.csv')[0]+ "_ground_truth.csv"))
            detected = pd.read_csv(os.path.join(directory_detected, filename.split('.csv')[0]+ "_detected.csv"))

        
            #detected
            #########   DOTS FOR WHAT IT'S SUPPOSED TO BE  #####################
            TOs_old = detected[detected.columns[0]]
            TOs_old = TOs_old.values.tolist()
            TOg_old = detected[detected.columns[1]]
            TOg_old = TOg_old.values.tolist()
            ICs_old = detected[detected.columns[2]]
            ICs_old = ICs_old.values.tolist()
            ICg_old = detected[detected.columns[3]]
            ICg_old = ICg_old.values.tolist()
            ogTOs_old = detected[detected.columns[4]]
            ogTOs_old = ogTOs_old.values.tolist()
            ogTOg_old = detected[detected.columns[5]]
            ogTOg_old = ogTOg_old.values.tolist()
            ogICs_old = detected[detected.columns[6]]
            ogICs_old = ogICs_old.values.tolist()
            ogICg_old = detected[detected.columns[7]]
            ogICg_old = ogICg_old.values.tolist()

            ##############################Filtering Nans out of Ground truth
            groundTO = []
            groundIC = []
            for i in range(0, len(TOs_old)):
                if TOs_old[i] == TOs_old[i]:
                    groundTO.append(TOs_old[i])
            for i in range(0, len(ICs_old)):
                if ICs_old[i] == ICs_old[i]:
                    groundIC.append(ICs_old[i])

            ICs = []
            ICg = []
            TOs = []
            TOg = []
            ogICs = []
            ogICg = []
            ogTOs = []
            ogTOg = []
            for i in range(0, len(TOs_old)):
                if TOs_old[i] == TOs_old[i]:
                    TOs.append(TOs_old[i]) # deleting NaNs
                    TOg.append(TOg_old[i]) # deleting NaNs
            for i in range(0, len(ICs_old)):
                if ICs_old[i] == ICs_old[i]:
                    ICs.append(ICs_old[i]) # deleting NaNs
                    ICg.append(ICg_old[i]) # deleting NaNs

            for i in range(0, len(ogTOs_old)):
                if ogTOs_old[i] == ogTOs_old[i]:
                    ogTOs.append(ogTOs_old[i]) # deleting NaNs
                    ogTOg.append(ogTOg_old[i]) # deleting NaNs
            for i in range(0, len(ogICs_old)):
                if ogICs_old[i] == ogICs_old[i]:
                    ogICs.append(ogICs_old[i]) # deleting NaNs
                    ogICg.append(ogICg_old[i]) # deleting NaNs


           #detect error and points missed
            TOerror = []
            TOmisses = 0
            if_got_point = True
            for i in range(1, len(groundTO)):
                if not if_got_point:
                    TOmisses+=1
                if_got_point = False
                for j in range(0,len(TOs) ):
                    if abs(groundTO[i]-TOs[j]) < 200:
                        TOerror.append(groundTO[i]-TOs[j])
                        if_got_point = True
            
            ICerror = []
            ICmisses = 0
            if_got_point = True
            for i in range(1, len(groundIC)):
                if not if_got_point:
                    ICmisses+=1
                if_got_point = False
                for j in range(0,len(ICs) ):
                    if abs(groundIC[i]-ICs[j]) < 200:
                        ICerror.append(groundIC[i]-ICs[j])
                        if_got_point = True

            if len(ICerror)==0 or len(TOerror)==0:
                print("Error in file: ", filename)
                print("Length of IC errors: ", len(ICerror), "; Length of TO errors: ", len(TOerror))
                continue

            if name[1] == "slow":
                overallICslow.append(sum(ICerror)/len(ICerror))
                overallTOslow.append(sum(TOerror)/len(TOerror))
            elif name[1] == "med":
                overallICmed.append(sum(ICerror)/len(ICerror))
                overallTOmed.append(sum(TOerror)/len(TOerror))
            elif name[1] == "fast":
                overallICfast.append(sum(ICerror)/len(ICerror))
                overallTOfast.append(sum(TOerror)/len(TOerror))
            elif name[1] == "vary":
                overallICvary.append(sum(ICerror)/len(ICerror))
                overallTOvary.append(sum(TOerror)/len(TOerror))
            writer.writerow([filename, sum(TOerror)/len(TOerror), sum(ICerror)/len(ICerror),TOmisses, ICmisses,(sum(ogTOs)-sum(groundTO))/len(ogTOs), (sum(ogICs)-sum(groundIC))/len(ogICs)])
            writer.writerow(groundTO)
            writer.writerow(TOs)
            writer.writerow(groundIC)
            writer.writerow(ICs)
            writer.writerow([])
    writer.writerow(["overallTOslow: ", "overallICslow: ", "overallTOmed: ", "overallICmed: ", "overallTOfast: ", "overallICfast: ", "overallTOvary: ", "overallICvary: "])
    writer.writerow([sum(overallTOslow)/len(overallTOslow), sum(overallICslow)/len(overallICslow),sum(overallTOmed)/len(overallTOmed), sum(overallICmed)/len(overallICmed), sum(overallTOfast)/len(overallTOfast), sum(overallICfast)/len(overallICfast), sum(overallTOvary)/len(overallTOvary), sum(overallICvary)/len(overallICvary) ])
    writer.writerow([])
    writer.writerow([ "Over all TO delay:", "Over all IC delay: "])
    THE_TO_delay = (sum(overallTOslow)/len(overallTOslow)+sum(overallTOmed)/len(overallTOmed)+sum(overallTOfast)/len(overallTOfast)+sum(overallTOvary)/len(overallTOvary))/4
    THE_IC_delay = (sum(overallICslow)/len(overallICslow)+sum(overallICmed)/len(overallICmed)+sum(overallICfast)/len(overallICfast)+sum(overallICvary)/len(overallICvary))/4
    writer.writerow([THE_TO_delay, THE_IC_delay])
    writer.writerow([])




    ################################################################
    ####################Plotting error##############################
    plt.figure(figsize=(8, 5))
    plt.rcParams.update({'font.size': 20})
    plt.scatter( [0]*len(overallTOslow), overallTOslow, label="Slow",color='green', linewidth=1.0, zorder=1)
    plt.scatter([1]*len(overallTOmed),  overallTOmed, label="Medium",color='orange', linewidth=1.0, zorder=1)
    plt.scatter( [2]*len(overallTOfast), overallTOfast, label="Fast",color='red', linewidth=1.0, zorder=1)
    plt.scatter( [3]*len(overallTOvary), overallTOvary, label="Varied",color='blue', linewidth=1.0, zorder=1)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.ylabel("Time (ms)")
    plt.title("TO Delay")
    plt.show()

    plt.figure(figsize=(8, 5))
    plt.rcParams.update({'font.size': 20})
    plt.scatter( [0]*len(overallICslow), overallICslow, label="Slow",color='green', linewidth=1.0, zorder=1)
    plt.scatter([1]*len(overallICmed),  overallICmed, label="Medium",color='orange', linewidth=1.0, zorder=1)
    plt.scatter( [2]*len(overallICfast), overallICfast, label="Fast",color='red', linewidth=1.0, zorder=1)
    plt.scatter( [3]*len(overallICvary), overallICvary, label="Varied",color='blue', linewidth=1.0, zorder=1)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.ylabel("Time (ms)")
    plt.title("IC Delay")
    plt.show()





