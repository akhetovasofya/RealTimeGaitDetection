#Thoughts:
# 1. put calibration protection to make sure calibration step was good




import pandas as pd
import csv
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd
from patsy import dmatrices
from statsmodels.tsa.ar_model import AutoReg

prev_point = 0
prev_time = 0
# Open the CSV file

with open("medium50m1excel.csv", "r") as file:
    # Create a CSV reader
    imu = csv.reader(file)

    # Skip the header row
    next(imu)

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

    plt.figure(figsize=(13, 5))
    plt.rcParams.update({'font.size': 20})
    

    # Iterate through each row
    for index, row in enumerate(imu):
        # Access individual values by index
        #print(row[9], row[6])
        if index<250:
            continue


        current_point = float(row[6])*-1
        #print(row)
        current_time = float(row[9])

        #if current_time<10000 or current_time>19000:
            #continue

        #CALIBRATION has a step cycle and it will record it from first sign change to 3rd sign change
        #if neg, wait until 0 and record until the next next 0
        #if pos, wait until 0 then record until the next next 0
        
        callibration[step%2].append(current_point)
        callibration_time[step%2].append(current_time)
        

        

        #recording swing and stance
        #if 0 or sign change, then start recording.
        if ((current_point==0.0)|((abs(prev_point)+abs(current_point))>abs(prev_point+current_point))): 
            
            if (((current_point==0.0)|((abs(prev_point)+abs(current_point))>abs(prev_point+current_point)))&second_zero):
                
                #elapsed_time = callibration_time[step%2][-1]-callibration_time[step%2][0]
                #check that it is a third 0
                #if (not calibrated)or (calibrated & ((elapsed_time/(sum(total_time)/len(total_time)))>0.7)):
                if True:
                    second_zero = False
                    first_zero = False
                    if (len(callibration[step%2])>0):
                        #print("STEP FINISHED")
                        
                        if calibrated:
                            param = AutoReg(callibration[step%2], lags = 15, exog = callibration_time[step%2]).fit()
                            print(callibration_time[step%2][-1])
                            prediction = param.predict(start=0, end=2000, dynamic=False, exog=callibration_time[step%2], exog_oos=None)
                            plt.plot(callibration_time[step%2], prediction, label="Prediction", linewidth=2.0, zorder=-1)
                            plt.plot(callibration_time[step%2], callibration[step%2], label="Recorded", linewidth=1.0, zorder=-1)
                            plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
                            plt.xlabel("Time (ms)")
                            plt.title("Auto-Regression Predicted vs Recorded Step")
                            plt.show()
                            break
                        calibrated = True
                        step+=1 #done with recording
                        #if (not calibrated):
                                #good trial so put it's values
                            #pos_peak.append(max(callibration[step%2]))
                            #TOpeak.append(min(callibration[step%2]))
                            #total_time.append(elapsed_time)
                            #standing_time.append(callibration_time[step%2][-1] - second_zero_time)
                            #index_mid_peak = callibration_time[step%2].index(second_zero_time)
                            #index_end_peak = int((len(callibration_time[step%2]) - index_mid_peak)/2)+index_mid_peak
                           # mid_peak_time_frame = callibration[step%2][index_mid_peak:index_end_peak]
                            #ICpeak.append(min(mid_peak_time_frame))
                            #print(elapsed_time)
                            #if step!=0 : #and elapsed_time>1250
                                #timing = [calib_time-callibration_time[step%2][0] for calib_time in callibration_time[step%2]]
                                #plt.plot(timing, callibration[step%2],  label="Step at {}".format(callibration_time[step%2][0]), linewidth=3.0)
                        

                        #taking out old
                        #if len(total_time)>3:
                            #pos_peak.pop(0)
                            #TOpeak.pop(0)
                            #total_time.pop(0)
                            #standing_time.pop(0)
                            #ICpeak.pop(0)
                    #callibration[step%2].clear()
                    #callibration_time[step%2].clear()
                    #print("cleared")
                continue

            #filetring post heel strike noise
            #SECOND 0 THAT WE IGNORE
            if (((current_point==0.0)|((abs(prev_point)+abs(current_point))>abs(prev_point+current_point)))&first_zero&(not second_zero)):
                second_zero = True# got to 2nd but we keep recording
                second_zero_time = current_time
            first_zero = True
        prev_point = current_point
        prev_time = current_time

#print("time")
##print(time)
#print("gyro")
#print(gyro)
#param = AutoReg(gyro, lags = 15, exog = time).fit()
#prediction = param.predict(start=None, end=None, dynamic=False, exog=None, exog_oos=None)
#print(prediction)
#print(len(prediction))



