import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import csv
import global_variables
import statistics
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

    #plotting delays
    fig, axs = plt.subplots(2, 4)   
    axs[0, 0].set_title('TO Delay in Slow')
    axs[0, 1].set_title('TO Delay in Medium')
    axs[0, 2].set_title('TO Delay in Fast')
    axs[0, 3].set_title('TO Delay in Vary')

    axs[1, 0].set_title('IC Delay in Slow')
    axs[1, 1].set_title('IC Delay in Medium')
    axs[1, 2].set_title('IC Delay in Fast')
    axs[1, 3].set_title('IC Delay in Vary')


    for filename in os.listdir(directory):
        # Check if the file is a .log file

        if filename.endswith(".csv"):
            name = filename.split('_')
            print(filename)
            if name[0] == "GRT03":
                continue
            imu = pd.read_csv(os.path.join(directory, filename))
            ground_truth = pd.read_csv(os.path.join(directory_ground_truth, filename.split('.csv')[0]+ "_ground_truth.csv"))
            detected = pd.read_csv(os.path.join(directory_detected, filename.split('.csv')[0]+ "_detected.csv"))

        
            #Values from detected
            peaks_value = detected[detected.columns[0]]
            peaks_value = peaks_value.values.tolist()
            peaks_time = detected[detected.columns[1]]
            peaks_time = peaks_time.values.tolist()
            ICdetected_value = detected[detected.columns[2]]
            ICdetected_value = ICdetected_value.values.tolist()
            ICdetected_time = detected[detected.columns[3]]
            ICdetected_time = ICdetected_time.values.tolist()
            TOdetected_value = detected[detected.columns[4]]
            TOdetected_value = TOdetected_value.values.tolist()
            TOdetected_time = detected[detected.columns[5]]
            TOdetected_time = TOdetected_time.values.tolist()
            ICshouldve_value = detected[detected.columns[6]]
            ICshouldve_value = ICshouldve_value.values.tolist()
            ICshouldve_time = detected[detected.columns[7]]
            ICshouldve_time = ICshouldve_time.values.tolist()
            TOshouldve_value = detected[detected.columns[8]]
            TOshouldve_value = TOshouldve_value.values.tolist()
            TOshouldve_time = detected[detected.columns[9]]
            TOshouldve_time = TOshouldve_time.values.tolist()
            ICdelay = detected[detected.columns[10]]
            ICdelay = ICdelay.values.tolist()
            TOdelay = detected[detected.columns[11]]
            TOdelay = TOdelay.values.tolist()
            init_ICdetected_value = detected[detected.columns[12]]
            init_ICdetected_value = init_ICdetected_value.values.tolist()
            init_ICdetected_time = detected[detected.columns[13]]
            init_ICdetected_time = init_ICdetected_time.values.tolist()
            init_TOdetected_value = detected[detected.columns[14]]
            init_TOdetected_value = init_TOdetected_value.values.tolist()
            init_TOdetected_time = detected[detected.columns[15]]
            init_TOdetected_time = init_TOdetected_time.values.tolist()
            

            #Values from ground truth
            TOs_truth = ground_truth[ground_truth.columns[0]]
            TOs_truth = TOs_truth.values.tolist()
            ICs_truth = ground_truth[ground_truth.columns[1]]
            ICs_truth = ICs_truth.values.tolist()
            

            #FILTERING OUT NaNs in ground truth
            checked_TOs_truth = []
            checked_ICs_truth = []
            for i in range(0, len(ICs_truth)):
                if ICs_truth[i] == ICs_truth[i]:
                    checked_ICs_truth.append(ICs_truth[i])
            for i in range(0, len(TOs_truth)):
                if TOs_truth[i] == TOs_truth[i]:
                    checked_TOs_truth.append(TOs_truth[i])

            #FILTERING OUT NaNs in detected
            checked_peaks_value = []
            checked_peaks_time = []
            checked_ICdetected_value = []
            checked_ICdetected_time = []
            checked_TOdetected_value = []
            checked_TOdetected_time = []
            checked_ICshouldve_value = []
            checked_ICshouldve_time = []
            checked_TOshouldve_value = []
            checked_TOshouldve_time = []
            checked_ICdelay = []
            checked_TOdelay = []
            checked_init_ICdetected_value = []
            checked_init_ICdetected_time = []
            checked_init_TOdetected_value = []
            checked_init_TOdetected_time = []

            for i in range(0, len(peaks_time)):
                if peaks_time[i] == peaks_time[i]:
                    checked_peaks_time.append(peaks_time[i]) # deleting NaNs
                    checked_peaks_value.append(peaks_value[i]) # deleting NaNs
            for i in range(0, len(ICdetected_value)):
                if ICdetected_value[i] == ICdetected_value[i]:
                    checked_ICdetected_value.append(ICdetected_value[i]) # deleting NaNs
                    checked_ICdetected_time.append(ICdetected_time[i]) # deleting NaNs
            for i in range(0, len(TOdetected_value)):
                if TOdetected_value[i] == TOdetected_value[i]:
                    checked_TOdetected_value.append(TOdetected_value[i]) # deleting NaNs
                    checked_TOdetected_time.append(TOdetected_time[i]) # deleting NaNs
            for i in range(0, len(ICshouldve_value)):
                if ICshouldve_value[i] == ICshouldve_value[i]:
                    checked_ICshouldve_value.append(ICshouldve_value[i]) # deleting NaNs
                    checked_ICshouldve_time.append(ICshouldve_time[i]) # deleting NaNs
            for i in range(0, len(TOshouldve_value)):
                if TOshouldve_value[i] == TOshouldve_value[i]:
                    checked_TOshouldve_value.append(TOshouldve_value[i]) # deleting NaNs
                    checked_TOshouldve_time.append(TOshouldve_value[i]) # deleting NaNs
            for i in range(0, len(ICdelay)):
                if ICdelay[i] == ICdelay[i]:
                    checked_ICdelay.append(ICdelay[i]) # deleting NaNs
            for i in range(0, len(TOdelay)):
                if TOdelay[i] == TOdelay[i]:
                    checked_TOdelay.append(TOdelay[i]) # deleting NaNs
            for i in range(0, len(init_ICdetected_value)):
                if init_ICdetected_value[i] == init_ICdetected_value[i]:
                    checked_init_ICdetected_value.append(init_ICdetected_value[i]) # deleting NaNs
                    checked_init_ICdetected_time.append(init_ICdetected_time[i]) # deleting NaNs
            for i in range(0, len(init_TOdetected_value)):
                if init_TOdetected_value[i] == init_TOdetected_value[i]:
                    checked_init_TOdetected_value.append(init_TOdetected_value[i]) # deleting NaNs
                    checked_init_TOdetected_time.append(init_TOdetected_time[i]) # deleting NaNs   
            
            

           #detect error and points missed
            TOerror = []
            TOmisses = 0
            if_got_point = True
            for i in range(1, len(TOs_truth)):
                if not if_got_point:
                    TOmisses+=1
                if_got_point = False
                for j in range(0,len(checked_TOdetected_time) ):
                    if abs(TOs_truth[i]-checked_TOdetected_time[j]) < 200:
                        TOerror.append(TOs_truth[i]-checked_TOdetected_time[j])
                        if_got_point = True
            
            ICerror = []
            ICmisses = 0
            if_got_point = True
            for i in range(1, len(ICs_truth)):
                if not if_got_point:
                    ICmisses+=1
                if_got_point = False
                for j in range(0,len(checked_ICdetected_time) ):
                    if abs(ICs_truth[i]-checked_ICdetected_time[j]) < 200:
                        ICerror.append(ICs_truth[i]-checked_ICdetected_time[j])
                        if_got_point = True

            if len(ICerror)==0 or len(TOerror)==0:
                print("Error in file: ", filename)
                print("Length of IC errors: ", len(ICerror), "; Length of TO errors: ", len(TOerror))
                continue

            if name[1] == "slow":
                overallICslow.append(sum(ICerror)/len(ICerror))
                overallTOslow.append(sum(TOerror)/len(TOerror))
                speed=0
            elif name[1] == "med":
                overallICmed.append(sum(ICerror)/len(ICerror))
                overallTOmed.append(sum(TOerror)/len(TOerror))
                speed = 1
            elif name[1] == "fast":
                overallICfast.append(sum(ICerror)/len(ICerror))
                overallTOfast.append(sum(TOerror)/len(TOerror))
                speed = 2
            elif name[1] == "vary":
                overallICvary.append(sum(ICerror)/len(ICerror))
                overallTOvary.append(sum(TOerror)/len(TOerror))
                speed = 3
            writer.writerow([filename, sum(TOerror)/len(TOerror), sum(ICerror)/len(ICerror),TOmisses, ICmisses,(sum(TOs_truth)-sum(checked_TOdetected_value))/len(checked_TOdetected_value), (sum(ICs_truth)-sum(checked_ICdetected_value))/len(checked_ICdetected_value), statistics.mean(checked_TOdelay), statistics.stdev(checked_TOdelay),statistics.mean(checked_ICdelay), statistics.stdev(checked_ICdelay)])
            writer.writerow(checked_ICdetected_value)
            writer.writerow(checked_ICdetected_time)
            writer.writerow(checked_TOdetected_value)
            writer.writerow(checked_TOdetected_time)
            writer.writerow([])
            writer.writerow(checked_TOs_truth)
            writer.writerow(checked_ICs_truth)
            writer.writerow([])
            writer.writerow([])
            TOlen_dif = len(checked_TOshouldve_time)-len(checked_TOs_truth)
            IClen_dif = len(checked_ICshouldve_time)-len(checked_ICs_truth)
            print(filename)
            if TOlen_dif!=0:
                print("TOs_truth: ", len(np.array(TOs_truth)))
                print(TOs_truth)
                print("TOshouldve_time: ", len(np.array(TOshouldve_time)))
                print(TOshouldve_time)
                print("checked_TOs_truth: ", len(np.array(checked_TOs_truth)))
                print("checked_TOshouldve_time: ", len(np.array(checked_TOshouldve_time)))
                subtractTOdelay = np.subtract(np.array(checked_TOs_truth[:TOlen_dif]), np.array(checked_TOshouldve_time))
            else:
                subtractTOdelay = np.subtract(np.array(checked_TOs_truth), np.array(checked_TOshouldve_time))    
            if IClen_dif!=0:
                print("ICs_truth: ", len(np.array(ICs_truth)))
                print("ICshouldve_time: ", len(np.array(ICshouldve_time)))
                print("checked_ICs_truth: ", len(np.array(checked_ICs_truth)))
                print("checked_ICshouldve_time: ", len(np.array(checked_ICshouldve_time)))
                subtractICdelay = np.subtract(np.array(checked_ICs_truth[:IClen_dif]), np.array(checked_ICshouldve_time))
            else:
                subtractICdelay = np.subtract(np.array(checked_ICs_truth), np.array(checked_ICshouldve_time))    
            axs[0,speed].plot(subtractTOdelay, label=name[0])
            axs[1,speed].plot(subtractICdelay, label=name[0])

    writer.writerow(["overallTOslow: ", "overallICslow: ", "overallTOmed: ", "overallICmed: ", "overallTOfast: ", "overallICfast: ", "overallTOvary: ", "overallICvary: "])
    writer.writerow([sum(overallTOslow)/len(overallTOslow), sum(overallICslow)/len(overallICslow),sum(overallTOmed)/len(overallTOmed), sum(overallICmed)/len(overallICmed), sum(overallTOfast)/len(overallTOfast), sum(overallICfast)/len(overallICfast), sum(overallTOvary)/len(overallTOvary), sum(overallICvary)/len(overallICvary) ])
    writer.writerow([])
    writer.writerow([ "Over all TO delay:", "Over all IC delay: "])
    THE_TO_delay = (sum(overallTOslow)/len(overallTOslow)+sum(overallTOmed)/len(overallTOmed)+sum(overallTOfast)/len(overallTOfast)+sum(overallTOvary)/len(overallTOvary))/4
    THE_IC_delay = (sum(overallICslow)/len(overallICslow)+sum(overallICmed)/len(overallICmed)+sum(overallICfast)/len(overallICfast)+sum(overallICvary)/len(overallICvary))/4
    writer.writerow([THE_TO_delay, THE_IC_delay])
    writer.writerow([])



    ####################finishing plotting
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.show()

    ################################################################
    ####################Plotting error##############################
    axs[0,speed].show()

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





