import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import csv
import global_variables
import statistics
import itertools
import seaborn as sns
import pandas as pd
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

    #std per trial
    sd_trial_overallTOslow = []
    sd_trial_overallICslow = []
    sd_trial_overallTOmed = []
    sd_trial_overallICmed = []
    sd_trial_overallTOfast = []
    sd_trial_overallICfast = []
    sd_trial_overallTOvary = []
    sd_trial_overallICvary = []

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
    num_ic_slow = []
    num_to_slow = []
    num_ic_med = []
    num_to_med = []
    num_ic_fast = []
    num_to_fast = []
    num_ic_vary = []
    num_to_vary = []

    #overall table
    IC_Table = [[], [], [], []]
    TO_Table = [[], [], [], []]

    #plotting delays
    fig, axs = plt.subplots(2, 4)   
    axs[1, 0].set_title('TO Predicted Lead in Slow')
    axs[1, 1].set_title('TO Predicted Lead in Medium')
    axs[1, 2].set_title('TO Predicted Lead in Fast')
    axs[1, 3].set_title('TO Predicted Lead in Vary')

    axs[0, 0].set_title('IC Predicted Lead in Slow')
    axs[0, 1].set_title('IC Predicted Lead in Medium')
    axs[0, 2].set_title('IC Predicted Lead in Fast')
    axs[0, 3].set_title('IC Predicted Lead in Vary')


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
                sd_trial_overallICslow.append(np.std(ICerror))
                sd_trial_overallTOslow.append(np.std(TOerror))
                overallICslow_thresh.extend(ICerror_thresh)
                overallTOslow_thresh.extend(TOerror_thresh)
                avg_trial_overallICslow_thresh.append(np.mean(ICerror_thresh))
                avg_trial_overallTOslow_thresh.append(np.mean(TOerror_thresh))
                standing_time_slow.extend(checked_standing_time)
                num_strides_slow.append(len(checked_standing_time))
                num_ic_slow.append(len(ICerror))
                num_to_slow.append(len(TOerror))
                speed=0
            elif name[1] == "med":
                overallICmed.extend(ICerror)
                overallTOmed.extend(TOerror)
                avg_trial_overallICmed.append(np.mean(ICerror))
                avg_trial_overallTOmed.append(np.mean(TOerror))
                sd_trial_overallICmed.append(np.std(ICerror))
                sd_trial_overallTOmed.append(np.std(TOerror))
                overallICmed_thresh.extend(ICerror_thresh)
                overallTOmed_thresh.extend(TOerror_thresh)
                avg_trial_overallICmed_thresh.append(np.mean(ICerror_thresh))
                avg_trial_overallTOmed_thresh.append(np.mean(TOerror_thresh))
                standing_time_med.extend(checked_standing_time)
                num_strides_med.append(len(checked_standing_time))
                num_ic_med.append(len(ICerror))
                num_to_med.append(len(TOerror))
                speed = 1
            elif name[1] == "fast":
                overallICfast.extend(ICerror)
                overallTOfast.extend(TOerror)
                avg_trial_overallICfast.append(np.mean(ICerror))
                avg_trial_overallTOfast.append(np.mean(TOerror))
                sd_trial_overallICfast.append(np.std(ICerror))
                sd_trial_overallTOfast.append(np.std(TOerror))
                overallICfast_thresh.extend(ICerror_thresh)
                overallTOfast_thresh.extend(TOerror_thresh)
                avg_trial_overallICfast_thresh.append(np.mean(ICerror_thresh))
                avg_trial_overallTOfast_thresh.append(np.mean(TOerror_thresh))
                standing_time_fast.extend(checked_standing_time)
                num_strides_fast.append(len(checked_standing_time))
                num_ic_fast.append(len(ICerror))
                num_to_fast.append(len(TOerror))
                speed = 2
            elif name[1] == "vary":
                overallICvary.extend(ICerror)
                overallTOvary.extend(TOerror)
                avg_trial_overallICvary.append(np.mean(ICerror))
                avg_trial_overallTOvary.append(np.mean(TOerror))
                sd_trial_overallICvary.append(np.std(ICerror))
                sd_trial_overallTOvary.append(np.std(TOerror))
                overallICvary_thresh.extend(ICerror_thresh)
                overallTOvary_thresh.extend(TOerror_thresh)
                avg_trial_overallICvary_thresh.append(np.mean(ICerror_thresh))
                avg_trial_overallTOvary_thresh.append(np.mean(TOerror_thresh))
                standing_time_vary.extend(checked_standing_time)
                num_strides_vary.append(len(checked_standing_time))
                num_ic_vary.append(len(ICerror))
                num_to_vary.append(len(TOerror))
                speed = 3
            #recording values
            IC_Table[speed].append(ICerror)
            TO_Table[speed].append(TOerror)

            #to see the delay between truth and where in IMU it should've been.
            if len(checked_TOs_truth)==len(checked_TOshouldve_time):
                subtractTOdelay = np.subtract(np.array(checked_TOs_truth), np.array(checked_TOshouldve_time))    #keeping the last one incase it gets detected
            else:
                subtractTOdelay = np.subtract(np.array(checked_TOs_truth[0:-1]), np.array(checked_TOshouldve_time))    #skipping the last one because it doesn't get detected
            
            if len(checked_ICs_truth)==len(checked_ICshouldve_time):
                subtractICdelay = np.subtract(np.array(checked_ICs_truth), np.array(checked_ICshouldve_time))    #keeping the last one incase it gets detected
            else:
                subtractICdelay = np.subtract(np.array(checked_ICs_truth[0:-1]), np.array(checked_ICshouldve_time))    #skipping the last one because it doesn't get detected
            
            axs[1,speed].scatter(range(len(subtractTOdelay)), subtractTOdelay, label=name[0], s=6)
            axs[0,speed].scatter(range(len(subtractICdelay)), subtractICdelay, label=name[0], s=6)
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
            

    #getting averages, so each index is all speed data
    ICspeeds = []
    TOspeeds = []
    #getting by speeds
    for i in range(0,4):
        ICspeeds.append(list(itertools.chain.from_iterable(IC_Table[i])))
        TOspeeds.append(list(itertools.chain.from_iterable(TO_Table[i])))
    
    ICtrial = []
    TOtrial = []
    #getting by trials, so each index is all trial data
    for i in range(0,len(IC_Table[0])):
        list_of_lists_trial_ic = list(list(zip(*IC_Table))[i])
        ICtrial.append(list(itertools.chain.from_iterable(list_of_lists_trial_ic)))
        list_of_lists_trial_to = list(list(zip(*TO_Table))[i])
        TOtrial.append(list(itertools.chain.from_iterable(list_of_lists_trial_to)))

    writer.writerow(["overallTOslow: ", "overallICslow: ", "overallTOmed: ", "overallICmed: ", "overallTOfast: ", "overallICfast: ", "overallTOvary: ", "overallICvary: "])
    writer.writerow([np.mean(TOspeeds[0]), np.mean(ICspeeds[0]), np.mean(TOspeeds[1]), np.mean(ICspeeds[1]),np.mean(TOspeeds[2]), np.mean(ICspeeds[2]), np.mean(TOspeeds[3]), np.mean(ICspeeds[3])])
    writer.writerow([np.std(TOspeeds[0]), np.std(ICspeeds[0]), np.std(TOspeeds[1]), np.std(ICspeeds[1]),np.std(TOspeeds[2]), np.std(ICspeeds[2]), np.std(TOspeeds[3]), np.std(ICspeeds[3])])
    writer.writerow([])
    writer.writerow(["Avg Standing Time Slow", "Avg Number or Strides Slow", "Avg Standing Time Med", "Avg Number or Strides Med", "Avg Standing Time Fast", "Avg Number or Strides Fast", "Avg Standing Time Vary", "Avg Number or Strides Vary"])
    writer.writerow([np.mean(standing_time_slow), np.mean(num_strides_slow), np.mean(standing_time_med), np.mean(num_strides_med), np.mean(standing_time_fast), np.mean(num_strides_fast), np.mean(standing_time_vary), np.mean(num_strides_vary)])
    writer.writerow([ "Over all TO delay:","Std TO delay:", "Over all IC delay: ","Std IC delay: ", "Step Detection Rate TO: ", "Step Detection Rate IC: ","Step Detection Rate All: ", "Average Standing time: ", "Average amount of steps: "])
    THE_TO_delay = TOspeeds[0] + TOspeeds[1] + TOspeeds[2] + TOspeeds[3]
    THE_IC_delay = ICspeeds[0] + ICspeeds[1] + ICspeeds[2] + ICspeeds[3]
    THE_TO_delay_thresh = overallTOslow_thresh + overallTOmed_thresh + overallTOfast_thresh + overallTOvary_thresh
    THE_IC_delay_thresh = overallICslow_thresh + overallICmed_thresh + overallICfast_thresh + overallICvary_thresh
    THE_STANDING_TIME = standing_time_slow + standing_time_med + standing_time_fast + standing_time_vary
    THE_NUM_STRIDES = num_strides_slow+num_strides_med+num_strides_fast+num_strides_vary
    writer.writerow([np.mean(THE_TO_delay),np.std(THE_TO_delay),  np.mean(THE_IC_delay),np.std(THE_IC_delay), 1-to_event_misses/to_event_number, 1-ic_event_number/ic_event_number, 1-(to_event_misses+ic_event_misses)/(to_event_number+ic_event_number), np.mean(THE_STANDING_TIME), np.mean(THE_NUM_STRIDES)])
    writer.writerow([np.mean(THE_TO_delay_thresh),np.std(THE_TO_delay_thresh),  np.mean(THE_IC_delay_thresh),np.std(THE_IC_delay_thresh), 1-to_event_misses/to_event_number, 1-ic_event_misses/ic_event_number, 1-(to_event_misses+ic_event_misses)/(to_event_number+ic_event_number) ])
    writer.writerow(["Total Strides: ", to_event_number+ic_event_number])
    writer.writerow([to_event_number, ic_event_number])
    writer.writerow([len(THE_TO_delay), len(THE_IC_delay)])
    writer.writerow(["Total Stances: ", len(THE_STANDING_TIME)])
    writer.writerow([])
    writer.writerow([to_event_misses, to_event_number, ic_event_misses, ic_event_number])
    writer.writerow([])
    writer.writerow(["slow"])
    writer.writerow(avg_trial_overallICslow)
    writer.writerow(sd_trial_overallICslow)
    writer.writerow(avg_trial_overallTOslow)
    writer.writerow(sd_trial_overallTOslow)
    writer.writerow(num_ic_slow)
    writer.writerow(num_to_slow)
    writer.writerow([])
    writer.writerow(["med"])
    writer.writerow(avg_trial_overallICmed)
    writer.writerow(sd_trial_overallICmed)
    writer.writerow(avg_trial_overallTOmed)
    writer.writerow(sd_trial_overallTOmed)
    writer.writerow(num_ic_med)
    writer.writerow(num_to_med)
    writer.writerow([])
    writer.writerow(["fast"])
    writer.writerow(avg_trial_overallICfast)
    writer.writerow(sd_trial_overallICfast)
    writer.writerow(avg_trial_overallTOfast)
    writer.writerow(sd_trial_overallTOfast)
    writer.writerow(num_ic_fast)
    writer.writerow(num_to_fast)
    writer.writerow([])
    writer.writerow(["vary"])
    writer.writerow(avg_trial_overallICvary)
    writer.writerow(sd_trial_overallICvary)
    writer.writerow(avg_trial_overallTOvary)
    writer.writerow(sd_trial_overallTOvary)
    writer.writerow(num_ic_vary)
    writer.writerow(num_to_vary)
    writer.writerow([])
    writer.writerow([])
    writer.writerow(["IC by speed"])
    writer.writerow([np.mean(ICspeeds[0]), np.mean(ICspeeds[1]), np.mean(ICspeeds[2]), np.mean(ICspeeds[3])])
    writer.writerow([np.std(ICspeeds[0]), np.std(ICspeeds[1]), np.std(ICspeeds[2]), np.std(ICspeeds[3])])
    writer.writerow([len(ICspeeds[0]),len(ICspeeds[1]),len(ICspeeds[2]),len(ICspeeds[3])])
    writer.writerow([len(ICspeeds[0])+len(ICspeeds[1])+len(ICspeeds[2])+len(ICspeeds[3])])
    writer.writerow(["TO by speed"])
    writer.writerow([np.mean(TOspeeds[0]), np.mean(TOspeeds[1]), np.mean(TOspeeds[2]), np.mean(TOspeeds[3])])
    writer.writerow([np.std(TOspeeds[0]), np.std(TOspeeds[1]), np.std(TOspeeds[2]), np.std(TOspeeds[3])])
    writer.writerow([len(TOspeeds[0]),len(TOspeeds[1]),len(TOspeeds[2]),len(TOspeeds[3])])
    writer.writerow([len(TOspeeds[0])+len(TOspeeds[1])+len(TOspeeds[2])+len(TOspeeds[3])])
    writer.writerow([])
    writer.writerow(["IC by trials"])
    writer.writerow([np.mean(ICtrial[0]), np.mean(ICtrial[1]), np.mean(ICtrial[2]), np.mean(ICtrial[3]), np.mean(ICtrial[4]), np.mean(ICtrial[5]), np.mean(ICtrial[6]), np.mean(ICtrial[7])])
    writer.writerow([np.std(ICtrial[0]), np.std(ICtrial[1]), np.std(ICtrial[2]), np.std(ICtrial[3]), np.std(ICtrial[4]), np.std(ICtrial[5]), np.std(ICtrial[6]), np.std(ICtrial[7])])
    writer.writerow([len(ICtrial[0]),len(ICtrial[1]),len(ICtrial[2]),len(ICtrial[3]),len(ICtrial[4]),len(ICtrial[5]),len(ICtrial[6]),len(ICtrial[7])])
    writer.writerow([len(ICtrial[0])+len(ICtrial[1])+len(ICtrial[2])+len(ICtrial[3])+len(ICtrial[4])+len(ICtrial[5])+len(ICtrial[6])+len(ICtrial[7])])
    writer.writerow(["TO by trials"])
    writer.writerow([np.mean(TOtrial[0]), np.mean(TOtrial[1]), np.mean(TOtrial[2]), np.mean(TOtrial[3]), np.mean(TOtrial[4]), np.mean(TOtrial[5]), np.mean(TOtrial[6]), np.mean(TOtrial[7])])
    writer.writerow([np.std(TOtrial[0]), np.std(TOtrial[1]), np.std(TOtrial[2]), np.std(TOtrial[3]), np.std(TOtrial[4]), np.std(TOtrial[5]), np.std(TOtrial[6]), np.std(TOtrial[7])])
    writer.writerow([len(TOtrial[0]),len(TOtrial[1]),len(TOtrial[2]),len(TOtrial[3]),len(TOtrial[4]),len(TOtrial[5]),len(TOtrial[6]),len(TOtrial[7])])
    writer.writerow([len(TOtrial[0])+len(TOtrial[1])+len(TOtrial[2])+len(TOtrial[3])+len(TOtrial[4])+len(TOtrial[5])+len(TOtrial[6])+len(TOtrial[7])])
    writer.writerow([])


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

    #virables
    box_width = 0.3
    fornt_size = 10
    tick_size = 8
    tick_label_size = 8
    label_size = 15
    legend_size = 8

    #IC distributions
    fig, axs = plt.subplots(4, 1, figsize=(8, 30))

    # Plot distributions on each subplot using KDE
    sns.kdeplot(ICspeeds[0], ax=axs[0], label='Slow', color='blue', legend=True)
    sns.kdeplot(ICspeeds[1], ax=axs[1], label='Medium', color='green',legend=True)
    sns.kdeplot(ICspeeds[2], ax=axs[2], label='Fast', color='orange', legend=True)
    sns.kdeplot(ICspeeds[3], ax=axs[3], label='Vary', color='red', legend=True)
    plt.legend()
    
    # Add titles and legend
    axs[0].set_title('Distribution of IC in Slow Condition', fontsize=fornt_size)
    axs[1].set_title('Distribution of IC in Medium Condition', fontsize=fornt_size)
    axs[2].set_title('Distribution of IC in Fast Condition', fontsize=fornt_size)
    axs[3].set_title('Distribution of IC in Vary Condition', fontsize=fornt_size)

    #sizes
    for ax in axs:
        #ax.get_yaxis().set_visible(False)
        ax.tick_params(axis='y', which='major', labelsize=tick_size)
        ax.tick_params(axis='x', which='major', labelsize=tick_size)
        ax.set_ylabel('')
        ax.set_xlim(-60, 60)
        ax.set_ylim(0, 0.045)
        ax.legend(loc="upper right", prop={'size': legend_size})

    ax_slow = axs[0].twinx()
    ax_med = axs[1].twinx()
    ax_fast = axs[2].twinx()
    ax_vary = axs[3].twinx()

    box_plot = sns.boxplot(data=IC_Table[0], ax=ax_slow, orient='h', width=box_width, showfliers=False)  # Make boxplot vertically smaller by adjusting width
    box_plot.set_yticklabels(box_plot.get_yticks(), size = tick_label_size)
    box_plot = sns.boxplot(data=IC_Table[1], ax=ax_med, orient='h', width=box_width, showfliers=False)  # Make boxplot vertically smaller by adjusting width
    box_plot.set_yticklabels(box_plot.get_yticks(), size = tick_label_size)
    box_plot = sns.boxplot(data=IC_Table[2], ax=ax_fast, orient='h', width=box_width, showfliers=False)  # Make boxplot vertically smaller by adjusting width
    box_plot.set_yticklabels(box_plot.get_yticks(), size = tick_label_size)
    box_plot = sns.boxplot(data=IC_Table[3], ax=ax_vary, orient='h', width=box_width, showfliers=False)  # Make boxplot vertically smaller by adjusting width
    box_plot.set_yticklabels(box_plot.get_yticks(), size = tick_label_size)

    fig.text(0.5, 0.04, 'Value', ha='center', fontsize=label_size)
    fig.text(0.04, 0.5, 'Density', va='center', rotation='vertical', fontsize=label_size)
    fig.text(0.95, 0.5, 'Subject Number', va='center', rotation='vertical', fontsize=label_size)


    plt.subplots_adjust(hspace=0.5)  # Adjust the value as needed to increase or decrease spacing
    plt.show() 



    #TO distributions
    fig, axs = plt.subplots(4, 1, figsize=(8, 30))

    # Plot distributions on each subplot using KDE
    sns.kdeplot(TOspeeds[0], ax=axs[0], label='Slow', color='blue')
    sns.kdeplot(TOspeeds[1], ax=axs[1], label='Medium', color='green')
    sns.kdeplot(TOspeeds[2], ax=axs[2], label='Fast', color='orange')
    sns.kdeplot(TOspeeds[3], ax=axs[3], label='Vary', color='red')
    plt.legend()

    # Add titles and legend
    axs[0].set_title('Distribution of TO in Slow Condition', fontsize=fornt_size)
    axs[1].set_title('Distribution of TO in Medium Condition', fontsize=fornt_size)
    axs[2].set_title('Distribution of TO in Fast Condition', fontsize=fornt_size)
    axs[3].set_title('Distribution of TO in Vary Condition', fontsize=fornt_size)

    #sizes
    for ax in axs:
        #ax.get_yaxis().set_visible(False)
        ax.tick_params(axis='y', which='major', labelsize=tick_size)
        ax.tick_params(axis='x', which='major', labelsize=tick_size)
        ax.set_ylabel('')
        ax.set_xlim(-100, 100)
        ax.set_ylim(0, 0.025)
        ax.legend(loc="upper right", prop={'size': legend_size})

    ax_slow = axs[0].twinx()
    ax_med = axs[1].twinx()
    ax_fast = axs[2].twinx()
    ax_vary = axs[3].twinx()

    box_plot = sns.boxplot(data=TO_Table[0], ax=ax_slow, orient='h', width=box_width, showfliers=False)  # Make boxplot vertically smaller by adjusting width
    box_plot.set_yticklabels(box_plot.get_yticks(), size = tick_label_size)
    box_plot = sns.boxplot(data=TO_Table[1], ax=ax_med, orient='h', width=box_width, showfliers=False)  # Make boxplot vertically smaller by adjusting width
    box_plot.set_yticklabels(box_plot.get_yticks(), size = tick_label_size)
    box_plot = sns.boxplot(data=TO_Table[2], ax=ax_fast, orient='h', width=box_width, showfliers=False)  # Make boxplot vertically smaller by adjusting width
    box_plot.set_yticklabels(box_plot.get_yticks(), size = tick_label_size)
    box_plot = sns.boxplot(data=TO_Table[3], ax=ax_vary, orient='h', width=box_width, showfliers=False)  # Make boxplot vertically smaller by adjusting width
    box_plot.set_yticklabels(box_plot.get_yticks(), size = tick_label_size)

    fig.text(0.5, 0.04, 'Value', ha='center', fontsize=label_size)
    fig.text(0.04, 0.5, 'Density', va='center', rotation='vertical', fontsize=label_size)
    fig.text(0.95, 0.5, 'Subject Number', va='center', rotation='vertical', fontsize=label_size)


    plt.subplots_adjust(hspace=0.5)  # Adjust the value as needed to increase or decrease spacing
    plt.show() 



