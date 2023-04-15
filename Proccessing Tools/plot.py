import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import csv
# Set the directory path to search for .log files
directory = "C:/Users/aheto/Documents/research/recording FSR big 10 people study/DataProccessing"
for filename in os.listdir(directory):
    # Check if the file is a .log file
    if filename.endswith(".csv"):
        name = substrings = filename.split('_')
        if name[1] == "med":
            name[1] = "Medium"
        name = name[0].capitalize() + " " + name[1].capitalize()

        plt.figure(figsize=(20, 5))
        plt.rcParams.update({'font.size': 20})
        imu = pd.read_csv(os.path.join(directory, filename))

        plt.plot(imu[imu.columns[9]], imu[imu.columns[6]]*-1, label="Angular Velocity\n in Z (deg/s)", linewidth=1.0, zorder=-1)
        plt.plot(imu[imu.columns[9]], imu[imu.columns[7]], label="FSR Toe", linewidth=1.0, zorder=-1)
        #plt.plot(imu[imu.columns[9]], np.gradient(imu[imu.columns[7]]), label="FSR Toe Gradient", linewidth=1.0, zorder=-1)
        plt.plot(imu[imu.columns[9]], imu[imu.columns[8]], label="FSR Heel", linewidth=1.0, zorder=-1)
        #plt.plot(imu[imu.columns[9]], np.gradient(imu[imu.columns[8]]), label="FSR Heel Gradient", linewidth=1.0, zorder=-1)
        
        # Add labels and legend
        plt.xlabel("Time (ms)")
        plt.title(name)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))


        # Show the plot
        plt.show()

#slow
#IC = [1,1,1,1,1,1]
#ICtime = [43860, 45300, 46650, 48020, 49420, 50870]
#TO = [1, 1, 1, 1, 1, 1]
#TOtime = [42950, 44450, 45850, 47220, 48610, 50030]

#medium

#ICtime = [2784,3942,5090,6224,7363,8500,9626,10730,11859,12977,14095,15221,16336,17444,18524,19613,20702,21809,22916,24000,25099,26190,27276,28397,29507,30612,31735, 32840,33950,35068,36183, 37304,38422,39536,40654,41779,42900,44040,45161,46313,47441]
#IC = [1]*len(ICtime)
#TOtime = [3486,4615,5786,6917,8046,9188,10322,11430,12534,13663,14781,15920,17030,18114,19202,20302,21422,22506,23602,24688,25780,26879,27978,29107,30209,31332,32434,33526,34649,35775,36906, 38006, 39132, 40242, 41375,42506, 43611,44770, 45891,47028,48178]
#TO = [1]*len(TOtime)
#print(len(ICtime))
#print(len(TOtime))
#fast
#IC = [1,1,1,1,1]
#ICtime = [84046, 85049, 86015, 87018, 88021]
#TO = [1, 1, 1, 1, 1]
#TOtime = [84629, 85624, 86612, 87615, 88626]

#plt.scatter(ICtime, IC, label="IC", color='red', linewidth=1.0, zorder=1)
#plt.scatter(TOtime, TO, label="TO", color='purple', linewidth=1.0, zorder=1)



