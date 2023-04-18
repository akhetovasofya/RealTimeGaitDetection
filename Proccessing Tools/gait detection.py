#Thoughts:
# 1. put calibration protection to make sure calibration step was good




import pandas as pd
import os
import csv

import matplotlib.pyplot as plt
import queue


prev_point = 0
prev_time = 0
import global_variables
directory = global_variables.directory
directory_for_saving = global_variables.directory_detected
for filename in os.listdir(directory):
    
    if filename.endswith(".csv"):
        name = filename.split('.csv')[0]
        name_split = name.split("_")
        if name_split[-1]=="truth":
            continue
        #if name_split[0]!="becca":
            #continue
        with open(os.path.join(directory, filename), "r") as file:
            # Create a CSV reader
            imu = csv.reader(file)
            print(filename)
            # Skip the header row
            next(imu)
            next(imu)

            right_foot = 1
            if name_split[0] == "becca" or name_split[0] == "ryan" or name_split[0] == "patrick" or name_split[0] =="sofya" or  name_split[0] =="josh":
                right_foot=-1
            if name_split[0] == "madeleine" and name_split[-2]=="right":
                right_foot=-1
            # I need to divide it into 2 sections, calibrations and then analysis
            callibration_step1 = []
            callibration_step2 = []
            callibration_step3 = []
            callibration = [callibration_step1, callibration_step2, callibration_step3]
            callibration_time1 = []
            callibration_time2 = []
            callibration_time3 = []
            callibration_time = [callibration_time1,callibration_time2,callibration_time3]

            #hold only 3 steps at a time
            standing_time = []
            pos_peak = []
            ICpeak = []
            TOpeak = []
            total_time = []

            #for testing in time
            peak = [] #max peak
            TOs = []
            ICs = []
            minipeak = [] #peak between IC and TO

            #for graphing
            TOg = []
            ICg = []

            #
            first_zero = False
            second_zero = False
            step = 0
            time_from_IC=0

            calibrated = False
            at_max_peak = False
            toes_off = False
            heel_strike = False
            at_mini_peak = False
            approach_low_toe = False


            # Iterate through each row
            for index, row in enumerate(imu):
                # Access individual values by index
                #print(row[9], row[6])
                if index<250:
                    continue

                if len(row)<9:
                    continue

                current_point = float(row[6])*right_foot
                #print(row)
                current_time = float(row[9])


                #CALIBRATION has a step cycle and it will record it from first sign change to 3rd sign change
                #if neg, wait until 0 and record until the next next 0
                #if pos, wait until 0 then record until the next next 0
                
                callibration[step%2].append(current_point)
                callibration_time[step%2].append(current_time)
                

                

                #recording swing and stance
                #if 0 or sign change, then start recording.
                if ((current_point==0.0)|((abs(prev_point)+abs(current_point))>abs(prev_point+current_point))): 
                    if (((current_point==0.0)|((abs(prev_point)+abs(current_point))>abs(prev_point+current_point)))&second_zero):
                        second_zero = False
                        first_zero = False
                        elapsed_time = callibration_time[step%2][-1]-callibration_time[step%2][0]
                        if (len(callibration[step%2])>0):
                            

                            if (not calibrated)or((max(callibration[step%2])/(sum(pos_peak)/len(pos_peak))>0.2) & (min(callibration[step%2])/(sum(TOpeak)/len(TOpeak))>0.2) & (elapsed_time/(sum(total_time)/len(total_time))>0.1)):
                                    #good trial so put it's values
                                pos_peak.append(max(callibration[step%2]))
                                TOpeak.append(min(callibration[step%2]))
                                total_time.append(elapsed_time)
                                standing_time.append(callibration_time[step%2][-1] - second_zero_time)
                                index_mid_peak = callibration_time[step%2].index(second_zero_time)
                                index_end_peak = int((len(callibration_time[step%2]) - index_mid_peak)/2)+index_mid_peak
                                mid_peak_time_frame = callibration[step%2][index_mid_peak:index_end_peak]
                                ICpeak.append(min(mid_peak_time_frame))
                                if step!=0 and elapsed_time>1250:
                                    timing = [calib_time-callibration_time[step%2][0] for calib_time in callibration_time[step%2]]
                                    plt.plot(timing, callibration[step%2],  label="Step at {}".format(callibration_time[step%2][0]), linewidth=3.0)
                                calibrated = True
                                step+=1 #done with recording

                            #taking out old
                            if len(total_time)>3:
                                pos_peak.pop(0)
                                TOpeak.pop(0)
                                total_time.pop(0)
                                standing_time.pop(0)
                                ICpeak.pop(0)
                        callibration[step%2].clear()
                        callibration_time[step%2].clear()
                        #print("cleared")
                        continue
                    if (((current_point==0.0)|((abs(prev_point)+abs(current_point))>abs(prev_point+current_point)))&first_zero):
                        second_zero = True# got to 2nd but we keep recording
                        second_zero_time = current_time
                    first_zero = True

                #THIS IS WHERE DECISIONS HAPPENED
                if (calibrated):
                    #peak
                    #at max peak
                    if ((current_point>sum(pos_peak)/len(pos_peak)*0.7)&(not at_max_peak)):
                        at_max_peak = True
                        toes_off = False
                        heel_strike = False
                        at_mini_peak = False
                        approach_low_toe = False
                        peak.append(current_time)
                    #what happend is threshold is bad for currernt
                    #at heel strike
                    elif ((current_point<sum(ICpeak)/len(ICpeak)*0.7)&at_max_peak):
                        heel_strike = True
                        at_max_peak = False
                        ICs.append(current_time)
                        ICg.append(current_point)
                        time_from_IC = current_time

                    #mini peak (having a time contraint for noisy data)
                    elif ((current_point>sum(TOpeak)/len(TOpeak)*0.7)&heel_strike&(sum(standing_time)/len(standing_time)*0.3<(current_time-time_from_IC))):
                        heel_strike = False
                        at_mini_peak = True
                        minipeak.append(current_time)
                            
                    #approaaching the low
                    elif ((current_point<sum(TOpeak)/len(TOpeak)*0.7)&at_mini_peak):
                        at_mini_peak = False
                        approach_low_toe = True
                    #at toes off
                    elif ((current_point>sum(TOpeak)/len(TOpeak)*0.7)&approach_low_toe):
                        toes_off = True
                        approach_low_toe = False
                        TOs.append(current_time)
                        TOg.append(current_point)
                prev_point = current_point
                prev_time = current_time





        # Open a new CSV file for writing
        with open((os.path.join(directory_for_saving, name + "_detected.csv")), "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["TO time","TO value", "IC time", "IC value"])
            #if TO is longer than IC
            if len(TOs)>=len(ICs):
                for i in range(0,len(TOs)):
                    if i >=len(ICs):
                        writer.writerow([TOs[i], TOg[i], "", ""])
                    else:
                        writer.writerow([TOs[i], TOg[i], ICs[i], ICg[i]])
            else:
                for i in range(0,len(ICs)):
                    if i >=len(TOs):
                        writer.writerow(["","", ICs[i], ICg[i]])
                    else:
                        writer.writerow([TOs[i], TOg[i], ICs[i], ICg[i]])

