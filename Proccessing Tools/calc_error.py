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
to_event_misses = 0
to_event_number = 0
ic_event_misses = 0
ic_event_number = 0

with open((os.path.join(directory_final_calculations, "Final_Calculations.csv")), "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Which file:", "TO average delay", "IC average delay", "TO misses", "IC misses", "TO truth delay", "IC truth delay", "Average TO delay", "Standard Deviation TO delay", "Average IC delay", "Standard Deviation IC delay"])
    
    #predicted
    overallTOslow = []
    overallICslow = []
    overallTOmed = []
    overallICmed = []
    overallTOfast = []
    overallICfast = []
    overallTOvary = []
    overallICvary = []

    #threshold
    overallTOslow_thresh = []
    overallICslow_thresh = []
    overallTOmed_thresh = []
    overallICmed_thresh = []
    overallTOfast_thresh = []
    overallICfast_thresh = []
    overallTOvary_thresh = []
    overallICvary_thresh = []

    #average per trial
    avg_trial_overallTOslow = []
    avg_trial_overallICslow = []
    avg_trial_overallTOmed = []
    avg_trial_overallICmed = []
    avg_trial_overallTOfast = []
    avg_trial_overallICfast = []
    avg_trial_overallTOvary = []
    avg_trial_overallICvary = []

    #average per trial threshold
    avg_trial_overallTOslow_thresh = []
    avg_trial_overallICslow_thresh = []
    avg_trial_overallTOmed_thresh = []
    avg_trial_overallICmed_thresh = []
    avg_trial_overallTOfast_thresh = []
    avg_trial_overallICfast_thresh = []
    avg_trial_overallTOvary_thresh = []
    avg_trial_overallICvary_thresh = []

    #stride length and steps
    standing_time_slow = []
    num_strides_slow = []
    standing_time_med = []
    num_strides_med = []
    standing_time_fast = []
    num_strides_fast = []
    standing_time_vary = []
    num_strides_vary = []

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
            if name[0] == "GRT03" or name[0] == "GRT08"  :
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
            standing_time = detected[detected.columns[16]]
            standing_time = standing_time.values.tolist()
            

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
            checked_standing_time = []

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
                    checked_TOshouldve_time.append(TOshouldve_time[i]) # deleting NaNs
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
            for i in range(0, len(standing_time)):
                if standing_time[i] == standing_time[i]:
                    checked_standing_time.append(standing_time[i]) # deleting NaNs
            

           #detect error and points missed
            TOerror = []
            TOerror_thresh = []
            TOmisses = len(checked_TOs_truth) - len(checked_TOdetected_time) - 1
            ICerror = []
            ICerror_thresh = []
            ICmisses = len(checked_ICs_truth) - len(checked_ICdetected_time) - 1
            TOmisses_check = -1
            ICmisses_check = -1
            print("checking length: ", len(checked_TOs_truth) ," , ", len(checked_ICs_truth))
            print("checking length detected: ", len(checked_TOdetected_time) ," , ", len(checked_ICdetected_time))
            print("checking misses: ", TOmisses ," , ", ICmisses)
            #If we missed, we have to skip some points in calculation if delay
            if TOmisses >= 0:
                j = 0 #variable to iterate through detected
                k = 1 #variable for initial
                #j is to iterate through detected
                #Essentially what I want to do here is to iterate through detected and see if the delay is too big, if so this is the one that we missed.
                #we can use this to cross ref with the TOmisses/ICmisses number
                for i in range(1, len(checked_TOs_truth)):
                    if abs(checked_TOs_truth[i]-checked_TOdetected_time[j])<300: #this means that it's a hit
                        TOerror.append(checked_TOs_truth[i]-checked_TOdetected_time[j])
                        while not abs(checked_init_TOdetected_time[k]-checked_TOdetected_time[j])<300: #this means that it's a hit
                            k+=1
                        TOerror_thresh.append(checked_TOs_truth[i]-checked_init_TOdetected_time[k])    
                        j+=1 #we want to increase j here because we found the hit with checked. If not, we want to stay at the same detected point until we find the next fitting ground truth
                    TOmisses_check = i-j #to cross referance with TOmisses

            if ICmisses >= 0:
                j = 0 #variable to iterate through detected
                k = 1 #variable for initial
                #j is to iterate through detected
                #Essentially what I want to do here is to iterate through detected and see if the delay is too big, if so this is the one that we missed.
                #we can use this to cross ref with the TOmisses/ICmisses number
                for i in range(1, len(checked_ICs_truth)):
                    if abs(checked_ICs_truth[i]-checked_ICdetected_time[j])<300: #this means that it's a hit
                        ICerror.append(checked_ICs_truth[i]-checked_ICdetected_time[j])
                        ICerror_thresh.append(checked_ICs_truth[i]-checked_init_ICdetected_time[j+1])
                        #iterate until find it finds it's initial
                        while not abs(checked_init_ICdetected_time[k]-checked_ICdetected_time[j])<300: #this means that it's a hit
                            k+=1
                        ICerror_thresh.append(checked_ICs_truth[i]-checked_init_ICdetected_time[k])
                        j+=1 #we want to increase j here because we found the hit with checked. If not, we want to stay at the same detected point until we find the next fitting ground truth
                    ICmisses_check = i-j # to cross reference with ICmisses

            if TOmisses<0 or ICmisses<0:
                print()
                print("Error in file: ", filename)
                print("ERROR: TOmisses or ICmissses is less than 0")
                print()
                continue

            #checking if none detected
            if len(ICerror)==0 or len(TOerror)==0:
                print()
                print("Error in file: ", filename, " ICerror OR TOerror is 0!")
                print("Length of IC errors: ", len(ICerror), "; Length of TO errors: ", len(TOerror))
                print()
                continue

            #TO misses mismatch
            if TOmisses_check != TOmisses:
                print()
                print("Error in file: ", filename)
                print("ERROR: TO MISSES DON'T MATCH!")
                print("Length: ", TOmisses, " Algo: ", TOmisses_check)
                print()
                print()
            
            #IC misses mismatch
            if ICmisses_check != ICmisses:
                print()
                print("Error in file: ", filename)
                print("ERROR: IC MISSES DON'T MATCH!")
                print("Length: ", ICmisses, " Algo: ", ICmisses_check)
                print()

            #stride 
            if len(ICerror)!= len(checked_standing_time) or len(TOerror)!= len(checked_standing_time):
                print("ERROR WITH STRIDES")
                print("IC: ", len(ICerror), " TO: ", len(TOerror), " Strides: ", len(checked_standing_time))
            
            if name[1] == "slow":
                overallICslow.extend(ICerror)
                overallTOslow.extend(TOerror)
                avg_trial_overallICslow.append(np.mean(ICerror))
                avg_trial_overallTOslow.append(np.mean(TOerror))
                overallICslow_thresh.extend(ICerror_thresh)
                overallTOslow_thresh.extend(TOerror_thresh)
                avg_trial_overallICslow_thresh.append(np.mean(ICerror_thresh))
                avg_trial_overallTOslow_thresh.append(np.mean(TOerror_thresh))
                standing_time_slow.extend(checked_standing_time)
                num_strides_slow.append(len(checked_standing_time))
                
                speed=0
            elif name[1] == "med":
                overallICmed.extend(ICerror)
                overallTOmed.extend(TOerror)
                avg_trial_overallICmed.append(np.mean(ICerror))
                avg_trial_overallTOmed.append(np.mean(TOerror))
                overallICmed_thresh.extend(ICerror_thresh)
                overallTOmed_thresh.extend(TOerror_thresh)
                avg_trial_overallICmed_thresh.append(np.mean(ICerror_thresh))
                avg_trial_overallTOmed_thresh.append(np.mean(TOerror_thresh))
                standing_time_med.extend(checked_standing_time)
                num_strides_med.append(len(checked_standing_time))
                speed = 1
            elif name[1] == "fast":
                overallICfast.extend(ICerror)
                overallTOfast.extend(TOerror)
                avg_trial_overallICfast.append(np.mean(ICerror))
                avg_trial_overallTOfast.append(np.mean(TOerror))
                overallICfast_thresh.extend(ICerror_thresh)
                overallTOfast_thresh.extend(TOerror_thresh)
                avg_trial_overallICfast_thresh.append(np.mean(ICerror_thresh))
                avg_trial_overallTOfast_thresh.append(np.mean(TOerror_thresh))
                standing_time_fast.extend(checked_standing_time)
                num_strides_fast.append(len(checked_standing_time))
                speed = 2
            elif name[1] == "vary":
                overallICvary.extend(ICerror)
                overallTOvary.extend(TOerror)
                avg_trial_overallICvary.append(np.mean(ICerror))
                avg_trial_overallTOvary.append(np.mean(TOerror))
                overallICvary_thresh.extend(ICerror_thresh)
                overallTOvary_thresh.extend(TOerror_thresh)
                avg_trial_overallICvary_thresh.append(np.mean(ICerror_thresh))
                avg_trial_overallTOvary_thresh.append(np.mean(TOerror_thresh))
                standing_time_vary.extend(checked_standing_time)
                num_strides_vary.append(len(checked_standing_time))
                speed = 3




            #to see the delay between truth and where in IMU it should've been.
            if len(checked_TOs_truth)==len(checked_TOshouldve_time):
                subtractTOdelay = np.subtract(np.array(checked_TOs_truth), np.array(checked_TOshouldve_time))    #keeping the last one incase it gets detected
            else:
                subtractTOdelay = np.subtract(np.array(checked_TOs_truth[0:-1]), np.array(checked_TOshouldve_time))    #skipping the last one because it doesn't get detected
            
            if len(checked_ICs_truth)==len(checked_ICshouldve_time):
                subtractICdelay = np.subtract(np.array(checked_ICs_truth), np.array(checked_ICshouldve_time))    #keeping the last one incase it gets detected
            else:
                subtractICdelay = np.subtract(np.array(checked_ICs_truth[0:-1]), np.array(checked_ICshouldve_time))    #skipping the last one because it doesn't get detected
            
            axs[0,speed].scatter(range(len(subtractTOdelay)), subtractTOdelay, label=name[0], s=6)
            axs[1,speed].scatter(range(len(subtractICdelay)), subtractICdelay, label=name[0], s=6)
            #axs[0,speed].ylabel("ms")
            #axs[1,speed].ylabel("ms")

            #collect misses for overall detection success
            to_event_misses+=TOmisses
            ic_event_misses+=ICmisses
            to_event_number+=len(checked_TOs_truth)-1 #all but the first detection
            ic_event_number+=len(checked_ICs_truth)-1 #all but the first detection

            writer.writerow([filename, sum(TOerror)/len(TOerror), sum(ICerror)/len(ICerror),TOmisses, ICmisses,sum(subtractTOdelay)/len(subtractTOdelay), sum(subtractICdelay)/len(subtractICdelay), statistics.mean(checked_TOdelay), statistics.stdev(checked_TOdelay),statistics.mean(checked_ICdelay), statistics.stdev(checked_ICdelay)])
            writer.writerow(["detected"])
            writer.writerow(checked_TOdetected_value)
            writer.writerow(checked_TOdetected_time)
            writer.writerow(checked_ICdetected_value)
            writer.writerow(checked_ICdetected_time)
            writer.writerow(["initial"])
            writer.writerow(TOerror_thresh)
            writer.writerow(ICerror_thresh)
            writer.writerow(["should've"])
            writer.writerow(checked_TOshouldve_time)
            writer.writerow(checked_ICshouldve_time)
            writer.writerow(["truth"])
            writer.writerow(checked_TOs_truth)
            writer.writerow(checked_ICs_truth)
            writer.writerow(["delay"])
            writer.writerow(subtractTOdelay)
            writer.writerow(subtractICdelay)
            writer.writerow(["thresh error"])
            writer.writerow(TOerror_thresh)
            writer.writerow(ICerror_thresh)
            writer.writerow([])
            writer.writerow([])
            

    writer.writerow(["overallTOslow: ", "overallICslow: ", "overallTOmed: ", "overallICmed: ", "overallTOfast: ", "overallICfast: ", "overallTOvary: ", "overallICvary: "])
    writer.writerow([sum(overallTOslow)/len(overallTOslow), sum(overallICslow)/len(overallICslow),sum(overallTOmed)/len(overallTOmed), sum(overallICmed)/len(overallICmed), sum(overallTOfast)/len(overallTOfast), sum(overallICfast)/len(overallICfast), sum(overallTOvary)/len(overallTOvary), sum(overallICvary)/len(overallICvary) ])
    writer.writerow([])
    writer.writerow(["Avg Standing Time Slow", "Avg Number or Strides Slow", "Avg Standing Time Med", "Avg Number or Strides Med", "Avg Standing Time Fast", "Avg Number or Strides Fast", "Avg Standing Time Vary", "Avg Number or Strides Vary"])
    writer.writerow([np.mean(standing_time_slow), np.mean(num_strides_slow), np.mean(standing_time_med), np.mean(num_strides_med), np.mean(standing_time_fast), np.mean(num_strides_fast), np.mean(standing_time_vary), np.mean(num_strides_vary)])
    writer.writerow([ "Over all TO delay:","Std TO delay:", "Over all IC delay: ","Std IC delay: ", "Step Detection Rate TO: ", "Step Detection Rate IC: ","Step Detection Rate All: ", "Average Standing time: ", "Average amount of steps: "])
    THE_TO_delay = overallTOslow + overallTOmed + overallTOfast + overallTOvary
    THE_IC_delay = overallICslow + overallICmed + overallICfast + overallICvary
    THE_TO_delay_thresh = overallTOslow_thresh + overallTOmed_thresh + overallTOfast_thresh + overallTOvary_thresh
    THE_IC_delay_thresh = overallICslow_thresh + overallICmed_thresh + overallICfast_thresh + overallICvary_thresh
    THE_STANDING_TIME = standing_time_slow + standing_time_med + standing_time_fast + standing_time_vary
    THE_NUM_STRIDES = num_strides_slow+num_strides_med+num_strides_fast+num_strides_vary
    writer.writerow([np.mean(THE_TO_delay),np.std(THE_TO_delay),  np.mean(THE_IC_delay),np.std(THE_IC_delay), 1-to_event_misses/to_event_number, 1-ic_event_misses/ic_event_number, 1-(to_event_misses+ic_event_misses)/(to_event_number+ic_event_number), np.mean(THE_STANDING_TIME), np.mean(THE_NUM_STRIDES)])
    writer.writerow([np.mean(THE_TO_delay_thresh),np.std(THE_TO_delay_thresh),  np.mean(THE_IC_delay_thresh),np.std(THE_IC_delay_thresh), 1-to_event_misses/to_event_number, 1-ic_event_misses/ic_event_number, 1-(to_event_misses+ic_event_misses)/(to_event_number+ic_event_number) ])
    writer.writerow(["Total Strides: ", to_event_number+ic_event_number])
    writer.writerow([to_event_number, ic_event_number])
    writer.writerow([len(THE_TO_delay), len(THE_IC_delay)])
    writer.writerow(["Total Stances: ", len(THE_STANDING_TIME)])



    ####################finishing plotting
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.show()

    ################################################################
    ####################Plotting error##############################
    

    plt.figure(figsize=(8, 5))
    plt.rcParams.update({'font.size': 20})
    plt.scatter( [0]*len(avg_trial_overallTOslow), avg_trial_overallTOslow, label="Slow",color='green', linewidth=1.0, zorder=1)
    plt.scatter([1]*len(avg_trial_overallTOmed),  avg_trial_overallTOmed, label="Medium",color='orange', linewidth=1.0, zorder=1)
    plt.scatter( [2]*len(avg_trial_overallTOfast), avg_trial_overallTOfast, label="Fast",color='red', linewidth=1.0, zorder=1)
    plt.scatter( [3]*len(avg_trial_overallTOvary), avg_trial_overallTOvary, label="Varied",color='blue', linewidth=1.0, zorder=1)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.ylabel("Time (ms)")
    plt.title("TO Predicted Lead")
    plt.show()

    plt.figure(figsize=(8, 5))
    plt.rcParams.update({'font.size': 20})
    plt.scatter( [0]*len(avg_trial_overallICslow), avg_trial_overallICslow, label="Slow",color='green', linewidth=1.0, zorder=1)
    plt.scatter([1]*len(avg_trial_overallICmed),  avg_trial_overallICmed, label="Medium",color='orange', linewidth=1.0, zorder=1)
    plt.scatter( [2]*len(avg_trial_overallICfast), avg_trial_overallICfast, label="Fast",color='red', linewidth=1.0, zorder=1)
    plt.scatter( [3]*len(avg_trial_overallICvary), avg_trial_overallICvary, label="Varied",color='blue', linewidth=1.0, zorder=1)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.ylabel("Time (ms)")
    plt.title("IC Predicted Lead")
    plt.show()

    plt.figure(figsize=(8, 5))
    plt.rcParams.update({'font.size': 20})
    plt.scatter( [0]*len(avg_trial_overallTOslow_thresh), avg_trial_overallTOslow_thresh, label="Slow",color='green', linewidth=1.0, zorder=1)
    plt.scatter([1]*len(avg_trial_overallTOmed_thresh),  avg_trial_overallTOmed_thresh, label="Medium",color='orange', linewidth=1.0, zorder=1)
    plt.scatter( [2]*len(avg_trial_overallTOfast_thresh), avg_trial_overallTOfast_thresh, label="Fast",color='red', linewidth=1.0, zorder=1)
    plt.scatter( [3]*len(avg_trial_overallTOvary_thresh), avg_trial_overallTOvary_thresh, label="Varied",color='blue', linewidth=1.0, zorder=1)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.ylabel("Time (ms)")
    plt.title("TO Threshold Lead")
    plt.show()

    plt.figure(figsize=(8, 5))
    plt.rcParams.update({'font.size': 20})
    plt.scatter( [0]*len(avg_trial_overallICslow_thresh), avg_trial_overallICslow_thresh, label="Slow",color='green', linewidth=1.0, zorder=1)
    plt.scatter([1]*len(avg_trial_overallICmed_thresh),  avg_trial_overallICmed_thresh, label="Medium",color='orange', linewidth=1.0, zorder=1)
    plt.scatter( [2]*len(avg_trial_overallICfast_thresh), avg_trial_overallICfast_thresh, label="Fast",color='red', linewidth=1.0, zorder=1)
    plt.scatter( [3]*len(avg_trial_overallICvary_thresh), avg_trial_overallICvary_thresh, label="Varied",color='blue', linewidth=1.0, zorder=1)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.ylabel("Time (ms)")
    plt.title("IC Threshold Lead")
    plt.show()





