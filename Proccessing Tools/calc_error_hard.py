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

with open((os.path.join(directory_final_calculations, "Final_Calculations_Hard.csv")), "w", newline="") as csvfile:
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
            print(filename)
            if name[0] == "GRT03":
                continue
            imu = pd.read_csv(os.path.join(directory, filename))
            ground_truth = pd.read_csv(os.path.join(directory_ground_truth, filename.split('.csv')[0]+ "_ground_truth.csv"))
            detected = pd.read_csv(os.path.join(directory_detected, filename.split('.csv')[0]+ "_hard_thresh_detected.csv"))
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

            ##############################################################################################
            ###############getting error#################################################################
            #deleting unused
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

            if ICs[0]>TOs[0]:
                first_detected = TOs[0]-200
            else:
                first_detected = ICs[0]-200
            
            if ICs[-1]>TOs[-1]:
                last_detected = ICs[-1]+200
            else:
                last_detected = TOs[-1]+200


            ICtime = []
            TOtime = []
            for ic_index in ICtime_old:
                if ic_index>first_detected and ic_index<last_detected:
                    ICtime.append(ic_index)
            for to_index in TOtime_old:
                if to_index>first_detected and to_index<last_detected:
                    TOtime.append(to_index)

            IC = [0]*len(ICtime)
            TO = [0]*len(TOtime)
            ######################################
            #for i in range(0, len(ICtime)):
                #difIC.append(ICtime[i]-ICs[i])
           # for i in range(0, len(TOtime)):
                #difTO.append(TOtime[i]-TOs[i])
            ICerror = (sum(ICtime)-sum(ICs))/len(ICs)
            TOerror = (sum(TOtime)-sum(TOs))/len(TOs)
            #print(TOs)
            #print(TOtime)
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
            writer.writerow(TOtime)
            writer.writerow(TOs)
            writer.writerow(ICtime)
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





