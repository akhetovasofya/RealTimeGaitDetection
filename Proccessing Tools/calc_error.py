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
    writer.writerow(["Which file:", "TO average delay", "IC average delay"])
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
        #if filename.split('_')[0] != "tyler":
        #    continue

        if filename.endswith(".csv"):
            name = filename.split('_')
            
            #####which trials we skipping#########
            if name[0] == "patrick" or name[0] == "siyang" or name[0] == "tyler":
                continue

            imu = pd.read_csv(os.path.join(directory, filename))
            ground_truth = pd.read_csv(os.path.join(directory_ground_truth, filename.split('.csv')[0]+ "_ground_truth.csv"))
            detected = pd.read_csv(os.path.join(directory_detected, filename.split('.csv')[0]+ "_detected.csv"))

            TOtime = ground_truth[ground_truth.columns[0]]
            ICtime = ground_truth[ground_truth.columns[1]]
        
            #detected
            #########   DOTS FOR WHAT IT'S SUPPOSED TO BE  #####################
            TOs = detected[detected.columns[0]]
            TOg = detected[detected.columns[1]]
            ICs = detected[detected.columns[2]]
            ICg = detected[detected.columns[3]]

            ##############################################################################################
            ###############getting error#################################################################

            #print(TOs)
            for i in range(0, len(TOtime)):
                if (TOs[0]-TOtime[i]) >200 or (TOtime[i] - TOs[len(TOs)-1])>200:
                    del TOtime[i]
            for i in range(0, len(TOtime)):
                if (ICs[0]-ICtime[i])>200 or (ICtime[i] - ICs[len(ICs)-1])>200:
                    del ICtime[i]
            IC = [0]*len(ICtime)
            TO = [0]*len(TOtime)
            ######################################
            difIC = []
            difTO = []
            for i in range(0, len(ICtime)):
                difIC.append(ICtime[i]-ICs[i])
            for i in range(0, len(TOtime)):
                difTO.append(TOtime[i]-TOs[i])
            ICerror = sum(difIC)/len(difIC)
            TOerror = sum(difTO)/len(difTO)
            if name[1] == "slow":
                overallICslow.append(ICerror)
                overallTOslow.append(TOerror)
            elif name[1] == "med":
                overallICmed.append(ICerror)
                overallTOmed.append(TOerror)
            elif name[1] == "fast":
                overallICfast.append(ICerror)
                overallTOfast.append(TOerror)
            elif name[1] == "vary":
                overallICvary.append(ICerror)
                overallTOvary.append(TOerror)
            writer.writerow([filename, TOerror, ICerror])
            writer.writerow([TOtime])
            writer.writerow([TOs])
            writer.writerow([ICtime])
            writer.writerow([ICs])
            writer.writerow([])
    writer.writerow(["overallTOslow: ", "overallICslow: ", "overallTOmed: ", "overallICmed: ", "overallTOfast: ", "overallICfast: ", "overallTOvary: ", "overallICvary: "])
    writer.writerow([sum(overallTOslow)/len(overallTOslow), sum(overallICslow)/len(overallICslow),sum(overallTOmed)/len(overallTOmed), sum(overallICmed)/len(overallICmed), sum(overallTOfast)/len(overallTOfast), sum(overallICfast)/len(overallICfast), sum(overallTOvary)/len(overallTOvary), sum(overallICvary)/len(overallICvary) ])
    writer.writerow([])
    writer.writerow([ "Over all TO delay:", "Over all IC delay: "])
    THE_TO_delay = (sum(overallTOslow)+sum(overallTOmed)+sum(overallTOfast)+sum(overallTOvary))/4
    THE_IC_delay = (sum(overallICslow)+sum(overallICmed)+sum(overallICfast)+sum(overallICvary))/4
    writer.writerow([THE_TO_delay, THE_IC_delay])
    writer.writerow([])





