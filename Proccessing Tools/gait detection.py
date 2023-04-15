#Thoughts:
# 1. put calibration protection to make sure calibration step was good




import pandas as pd

import csv

import matplotlib.pyplot as plt
import queue


prev_point = 0
prev_time = 0
# Open the CSV file
plt.figure(figsize=(20, 5))
plt.rcParams.update({'font.size': 20})

plt.title("Isolated Step")
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


    # Iterate through each row
    for index, row in enumerate(imu):
        # Access individual values by index
        #print(row[9], row[6])
        if index<250:
            continue


        current_point = float(row[6])*-1
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
                        print(elapsed_time)
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
            elif ((current_point<sum(ICpeak)/len(ICpeak)*0.8)&at_max_peak):
                heel_strike = True
                at_max_peak = False
                ICs.append(current_time)
                ICg.append(current_point)
                time_from_IC = current_time

            #mini peak (having a time contraint for noisy data)
            elif ((current_point>sum(TOpeak)/len(TOpeak)*0.3)&heel_strike&(sum(standing_time)/len(standing_time)*0.3<(current_time-time_from_IC))):
                heel_strike = False
                at_mini_peak = True
                minipeak.append(current_time)
                    
            #approaaching the low
            elif ((current_point<sum(TOpeak)/len(TOpeak)*0.8)&at_mini_peak):
                at_mini_peak = False
                approach_low_toe = True
            #at toes off
            elif ((current_point>sum(TOpeak)/len(TOpeak)*0.8)&approach_low_toe):
                toes_off = True
                approach_low_toe = False
                TOs.append(current_time)
                TOg.append(current_point)
        prev_point = current_point
        prev_time = current_time




####################################################################
#Values
####################################################################
#plt.savefig('Isolated Calibration step.png')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.show()
print("final answers")


####################################################################
#PRINTING DETECTED VALUES
####################################################################
print("Analysis")
print("peak")
print(peak)
print("TOs")
print(TOs)
print("ICs")
print(ICs)
print("TOg")
print(TOg)
print("ICg")
print(ICg)
print("minipeak")
print(minipeak)





####################################################################
#Plotting detection
####################################################################
# Read the CSV data into a pandas DataFrame

plt.figure(figsize=(13, 5))
plt.rcParams.update({'font.size': 20})
imu = pd.read_csv("medium50m1excel.csv")
#length = int(len(imu)*0.75)
imu = imu[250:]

plt.figure(figsize=(13, 5))
plt.plot(imu[imu.columns[9]], imu[imu.columns[6]]*-1, label="Angular Velocity\n in Z (deg/s)", linewidth=1.0, zorder=-1)
plt.plot(imu[imu.columns[9]], imu[imu.columns[7]], label="FSR Toe", linewidth=1.0, zorder=-1)
plt.plot(imu[imu.columns[9]], imu[imu.columns[8]], label="FSR Heel", linewidth=1.0, zorder=-1)
#########   DOTS FOR DETECTED  #####################
plt.scatter(ICs, ICg, label="Detected IC", color='red', zorder=2, linewidth=0.2)
plt.scatter(TOs, TOg, label="Detected TO", color='purple', zorder=2, linewidth=0.2)


##############################################################################
#######################   HAND PICKING THE POINTS#############################
#medium8
#IC = [1,1,1,1]
#ICtime = [ 144838-144390, 145979-144390, 147120-144390, 148267-144390]
#TO = [ 1, 1, 1, 1]
#TOtime = [ 145530-144390, 146641-144390, 147781-144390, 148983-144390]

#medium50
ICtime = [2784,3942,5090,6224,7363,8500,9626,10730,11859,12977,14095,15221,16336,17444,18524,19613,20702,21809,22916,24000,25099,26190,27276,28397,29507,30612,31735, 32840,33950,35068,36183, 37304,38422,39536,40654,41779,42900,44040,45161,46313,47441]
ICtime = ICtime[1:]# skip first for calibration
IC = [1]*len(ICtime)
TOtime = [3486,4615,5786,6917,8046,9188,10322,11430,12534,13663,14781,15920,17030,18114,19202,20302,21422,22506,23602,24688,25780,26879,27978,29107,30209,31332,32434,33526,34649,35775,36906, 38006, 39132, 40242, 41375,42506, 43611,44770, 45891,47028,48178]
TOtime = TOtime[1:]# skip first for calibration
TO = [1]*len(TOtime)

#########   DOTS FOR WHAT IT'S SUPPOSED TO BE  #####################
plt.scatter(ICtime, IC, marker='o',s=10, label="IC (from FSR)", facecolors='none', edgecolors='red',linewidth=1.0, zorder=1)
plt.scatter(TOtime, TO, marker='o',s=10, label="TO (from FSR)", facecolors='none', edgecolors='purple', linewidth=1.0, zorder=1)

##############################################################################
##############################################################################



# Add labels and legend
plt.xlabel("Time (ms)")
plt.title("Medium Walk")
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))


# Show the plot
plt.show()



##############################################################################
#######################   ERROR   ############################################
print("length TO and IC:")
print(len(TOs))
print(len(ICs))
print("AVERAGES:")
avergageIC  = (sum(ICtime)-sum(ICs))/len(ICs)
print("IC average delay: ")
print(avergageIC)
avergageTO  = (sum(TOtime)-sum(TOs))/len(TOs)
print("TO average delay: ")
print(avergageTO)
print("all errors")
theyis = []
difIC = []
difTO = []
print(len(ICtime))
for i in range(0, len(ICtime)):
    print("IC")
    print(ICtime[i]-ICs[i])
    difIC.append(ICtime[i]-ICs[i])
    print("TO")
    print(TOtime[i]-TOs[i])
    difTO.append(TOtime[i]-TOs[i])
    theyis.append(i)
plt.figure(figsize=(13, 5))
plt.plot(difIC, label="IC detection\n difference")
plt.plot(difTO, label="TO detection\n difference")
plt.ylabel("Time (ms)")
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.title("Detection difference")
plt.show()
##############################################################################
##############################################################################

