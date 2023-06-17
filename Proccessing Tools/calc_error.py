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
    writer.writerow(["Which file:", "TO average delay", "IC average delay", "TO misses", "IC misses"])
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
            #print(detected)
            TOtime_old = ground_truth[ground_truth.columns[0]]
            TOtime_old = TOtime_old.values.tolist()
            ICtime_old = ground_truth[ground_truth.columns[1]]
            ICtime_old = ICtime_old.values.tolist()
        
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

            ##############################Filtering Nans out of Ground truth
            groundTO = []
            groundIC = []
            for i in range(0, len(TOtime_old)):
                if TOtime_old[i] == TOtime_old[i]:
                    groundTO.append(TOtime_old[i])
            for i in range(0, len(ICtime_old)):
                if ICtime_old[i] == ICtime_old[i]:
                    groundIC.append(ICtime_old[i])

            ##############################################################################################
            ###############getting error#################################################################
            #deleting unused
            #deleting unused
            ICs = []
            ICg = []
            TOs = []
            TOg = []
            for i in range(0, len(TOs_old)):
                if TOs_old[i] == TOs_old[i]:
                    
                    if (groundTO[0]-TOs_old[i])<200 and (groundTO[-1]-TOs_old[i])>-200: #cutting off edges
                        TOs.append(TOs_old[i]) # deleting NaNs
                        TOg.append(TOg_old[i]) # deleting NaNs
                    else:
                        print("TO IF: 1st is ", groundTO[0]-TOs_old[i], " and 2nd is ", groundTO[-1]-TOs_old[i])
            for i in range(0, len(ICs_old)):
                if ICs_old[i] == ICs_old[i]:
                    if (groundIC[0]-ICs_old[i])<200 and (groundIC[-1]-ICs_old[i])>-200: #cutting off edges
                        ICs.append(ICs_old[i]) # deleting NaNs
                        ICg.append(ICg_old[i]) # deleting NaNs
                    else:
                        print("IC IF: 1st is ", groundIC[0]-ICs_old[i], " and 2nd is ", groundIC[-1]-ICs_old[i])


            if len(TOs) == 0 or len(ICs) == 0:
                print("ICs_old: ",ICs_old )
                print("ICs_old: ",TOs_old )
                print("ERRROR IN DETECTED")
                continue

           

           ################################################################################
           ##########################


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


            #print(TOs)
            #print(TOtime)
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
            writer.writerow([filename, sum(TOerror)/len(TOerror), sum(ICerror)/len(ICerror),TOmisses, ICmisses])
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





