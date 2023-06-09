#Thoughts:
# 1. put calibration protection to make sure calibration step was good




import pandas as pd
import os
import csv

import matplotlib.pyplot as plt
import queue


prev_point = 0
second_prev_point = 0
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
        with open(os.path.join(directory, filename), "r") as file:
            # Create a CSV reader
            imu = csv.reader(file)
            print()
            print()
            print(filename)
            # Skip the header row
            next(imu)
            next(imu)
            if name_split[0] == "GRT03" and name_split[0] !="GRT02_fast_01.csv":
                continue
            right_foot = 1
            if name_split[0] == "GRT07" or name_split[0] == "GRT09" or name_split[0] == "GRT05" or name_split[0] =="sofya" or  name_split[0] =="GRT02":
                right_foot=-1
            if name_split[0] == "GRT03" and name_split[-2]=="right":
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
            TOtime = []
            ICtime = []
            ICdelay = []
            TOdelay = []
            total_time = []

            #for testing in time
            peak = [] #max peak
            TOs = []
            ogTOs = []
            ogICg = []
            ICs = []
            minipeak = [] #peak between IC and TO

            #for graphing
            TOg = []
            ogTOg = []
            ogICs = []
            ICg = []

            #
            first_zero = False
            second_zero = False
            step = 0
            time_from_IC=0
            IC_min_point = 0

            calibrated = False
            at_max_peak = False
            toes_off = False
            heel_strike = False
            at_mini_peak = False
            approach_low_toe = False

            isTOdelya = False
            isICdelya = False
            waitingtime = 0
            goodTO = True
            goodIC = True


            # Iterate through each row
            for index, row in enumerate(imu):
                # Access individual values by index
                #print(row[9], row[6])

                #if index <200:
                #    continue
                if len(row)<9:
                    continue

                current_point = float(row[6])*right_foot
                #print(row)
                current_time = float(row[9])


                #CALIBRATION has a step cycle and it will record it from first sign change to 3rd sign change
                #if neg, wait until 0 and record until the next next 0
                #if pos, wait until 0 then record until the next next 0
                
                callibration[step%3].append(current_point)
                callibration_time[step%3].append(current_time)
                

                #recording swing and stance
                #if 0 or sign change, then start recording.
                if ((current_point==0.0)|((abs(prev_point)+abs(current_point))>abs(prev_point+current_point))): 
                    if (((current_point==0.0)|((abs(prev_point)+abs(current_point))>abs(prev_point+current_point)))&second_zero):
                        second_zero = False
                        first_zero = False
                        elapsed_time = callibration_time[step%3][-1]-callibration_time[step%3][0]
                        if (len(callibration[step%3])>0):
                            

                            if (not calibrated)or((max(callibration[step%3])/(sum(pos_peak)/len(pos_peak))>0.2) & (min(callibration[step%3])/(sum(TOpeak)/len(TOpeak))>0.2) & (elapsed_time/(sum(total_time)/len(total_time))>0.6)):
                                    #good trial so put it's values
                                print("calib time: ", callibration_time[step%3])
                                print("values: ", callibration[step%3] )
                                pos_peak.append(max(callibration[step%3]))
                                total_time.append(elapsed_time)
                                if calibrated:
                                    which_middle_index = callibration_time[step%3].index(minipeak[-1])
                                else:
                                    which_middle_index = int(len(callibration[step%3])/3*2)
                                print("which_middle_index: ", which_middle_index)
                                print("value at index : ", callibration[step%3][which_middle_index])
                                print("time at index : ", callibration_time[step%3][which_middle_index])
                                mid_peak_frame = callibration[step%3][0:which_middle_index]
                                mid_peak_frame_time = callibration_time[step%3][0:which_middle_index]
                                end_peak_frame = callibration[step%3][which_middle_index:-1]
                                end_peak_frame_time = callibration_time[step%3][which_middle_index:-1]

                                print("mid_peak_time_frame: ",mid_peak_frame )
                                print("end_peak_time_frame: ", end_peak_frame)

                                
                                TOpeak.append(min(end_peak_frame))
                                TOtime.append(end_peak_frame_time[end_peak_frame.index(TOpeak[-1])])
                                ICpeak.append(min(mid_peak_frame))
                                ICtime.append(mid_peak_frame_time[mid_peak_frame.index(ICpeak[-1])])
                                standing_time.append(TOtime[-1] - ICtime[-1])

                                print()
                                print("NEW AVERAGES: ")
                                print("TO: ",sum(TOpeak)/len(TOpeak) )
                                print(TOpeak)
                                print(TOtime)
                                print("IC: ",sum(ICpeak)/len(ICpeak) )
                                print(ICpeak)
                                print(ICtime)
                                if calibrated&(len(ICs)!=0)&(len(TOs)!=0):
                                    
                                    print("IC Delay: ", ICdelay)
                                    if callibration_time[step%3][callibration[step%3].index(ICpeak[-1])]-ogICs[-1]!=0:
                                        ICdelay.append(callibration_time[step%3][callibration[step%3].index(ICpeak[-1])]-ogICs[-1])
                                    print("IC Delay appended : ", ICdelay[-1])
                                    if goodTO:
                                        print()
                                        print("TO Delay: ", TOdelay)
                                        if callibration_time[step%3][callibration[step%3].index(TOpeak[-1])]-ogTOs[-1]!=0:
                                            TOdelay.append(callibration_time[step%3][callibration[step%3].index(TOpeak[-1])]-ogTOs[-1])
                                        print("TO Delay appended : ", TOdelay[-1])
                                    
                                calibrated = True
                                step+=1 #done with recording

                                #taking out old
                                if len(total_time)>3:
                                    pos_peak.pop(0)
                                    #TOpeak.pop(0)
                                    #TOtime.pop(0)
                                    total_time.pop(0)
                                    standing_time.pop(0)
                                    #ICpeak.pop(0)
                                    #ICtime.pop(0)
                                if len(ICdelay)>3:
                                    ICdelay.pop(0)
                                if len(TOdelay)>3:
                                    TOdelay.pop(0)
                                callibration[step%3].clear()
                                callibration_time[step%3].clear()
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
                        print()
                        print("AT PEAK")
                    #what happend is threshold is bad for currernt
                    #at heel strike
                    elif (current_point<(sum(ICpeak)/len(ICpeak)*0.8) or (((current_point - prev_point)>5 and (current_point-second_prev_point)>0) and current_point<0))&at_max_peak:
                        
                        if len(ICs)==0 or len(ICdelay)==0:
                            print("AT HEEL STRIKE")
                            ICs.append(current_time)
                            ICg.append(current_point)
                            heel_strike = True
                            at_max_peak = False
                            time_from_IC = current_time
                            ogICs.append(current_time)
                            ogICg.append(current_point)
                        elif isICdelya and (current_time-waitingtime)>(sum(ICdelay)/len(ICdelay)):
                            print("AT HEEL STRIKE")
                            print("Average time: ", (sum(ICdelay)/len(ICdelay)))
                            print("delay time: ", (current_time-waitingtime))
                            heel_strike = True
                            at_max_peak = False
                            time_from_IC = current_time
                            ICs.append(current_time)
                            ICg.append(current_point)
                            isICdelya = False
                        elif not isICdelya:
                            waitingtime = current_time
                            ogICs.append(current_time)
                            ogICg.append(current_point)
                            isICdelya = True
                        
                        

                    #mini peak (having a time contraint for noisy data)
                    #
                    elif (current_point>(sum(TOpeak)/len(TOpeak)*0.5))&heel_strike:
                        print("TIMES AT MINI PEAK: ", standing_time )
                        if (sum(standing_time)/len(standing_time)*0.3<(current_time-time_from_IC)):
                            heel_strike = False
                            at_mini_peak = True
                            print("AT MINI PEAK: ", current_time)
                            minipeak.append(current_time)
                          
                    #approaaching the low
                    elif ((current_point<(sum(TOpeak)/len(TOpeak)*0.8))&at_mini_peak):
                        if (current_time-time_from_IC)>sum(standing_time)/len(standing_time)*0.6:
                            #waiting for delay
                            if len(TOs)==0 or len(TOdelay)==0:
                                print("AT TO")
                                at_mini_peak = False
                                approach_low_toe = True
                                TOs.append(current_time)
                                TOg.append(current_point)
                                ogTOs.append(current_time)
                                ogTOg.append(0)
                                goodTO = True
                            elif isTOdelya and (current_time-waitingtime)>(sum(TOdelay)/len(TOdelay)):
                                print("AT TO")
                                print("Average time: ", (sum(TOdelay)/len(TOdelay)))
                                print("delay time: ", (current_time-waitingtime))
                                at_mini_peak = False
                                approach_low_toe = True
                                TOs.append(current_time)
                                TOg.append(current_point)
                                goodTO = True
                                isTOdelya = False
                            elif not isTOdelya:
                                ogTOs.append(current_time)
                                ogTOg.append(current_point)
                                isTOdelya = True
                                waitingtime = current_time
                                print("waitingtime: ", waitingtime)


                    #at toes off #saving if toe never went off so have a positive
                    if (((current_point>(sum(TOpeak)/len(TOpeak)))&((current_point - prev_point)>5))&at_mini_peak&((current_time-time_from_IC)>(sum(standing_time)/len(standing_time)))):
                        toes_off = True
                        print("AT TO SAFE POINT")
                        if not isTOdelya:
                            ogTOs.append(current_time)
                            ogTOg.append(0)
                        isTOdelya = False
                        at_mini_peak = False
                        approach_low_toe = False
                        print("Vel: ", (current_point - prev_point), " Time dif: ",(current_time-time_from_IC), " Needed time dif: ",(sum(standing_time)/len(standing_time)) )
                        TOs.append(current_time)
                        TOg.append(current_point)
                        goodTO = False
                        
                    #saving if toe never went off
                second_prev_point =prev_point
                prev_point = current_point
                prev_time = current_time
                   




        print()
        print("POINTS:")
        print("TOtime: ", TOtime)
        #print("peak: ", peak)
        print("ICs: ", ICs)
        print("TOs: ", TOs)
        print("ogTOs: ", ogTOs)
        print()
        print("LENGTHS:")
        print("ICs: ", len(ICs))
        print("TOs: ", len(TOs))
        print("ogTOs: ", len(ogTOs))
        #print("minipeak: ", minipeak)
        print()
        print("ICdelay: ",ICdelay)
        print("TOdelay: ", TOdelay)
        print()
        # Open a new CSV file for writing
        with open((os.path.join(directory_for_saving, name + "_detected.csv")), "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["TO time detected","TO value detected", "IC time detected", "IC value detected", "ogTO time","ogTO value","ogIC time","ogIC value"])
            #if TO is longer than IC
            longestTime = len(ICtime)
            if len(TOtime)>=len(ICtime):
                longestTime = len(TOtime)
            for i in range(0,longestTime):
                ogICputinS = ""
                ogICputinG = ""
                ogTOputinS = ""
                ogTOputinG = ""
                TOpeak_putin = ""
                TOtime_putin = ""
                ICpeak_putin = ""
                ICtime_putin = ""
                if i<len(ogICs):
                    ogICputinS = ogICs[i]
                    ogICputinG = ogICg[i]
                if i<len(ogTOs):
                    ogTOputinS = ogTOs[i]
                    ogTOputinG = ogTOg[i]
                if i <len(ICtime):
                    ICtime_putin = ICtime[i]
                    ICpeak_putin = ICpeak[i]
                if i <len(TOtime):
                    TOtime_putin = TOtime[i]
                    TOpeak_putin = TOpeak[i]
                writer.writerow([TOtime_putin, TOpeak_putin, ICtime_putin, ICpeak_putin, ogTOputinS, ogTOputinG, ogICputinS, ogICputinG])
        #
        #break

