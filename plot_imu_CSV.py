from datetime import datetime
import matplotlib as mpl
import matplotlib.animation as ani
import matplotlib.pyplot as plt
import pandas as pd

## returns the difference in seconds between timestamps using datetime
def timestampDiff(time1, time2):
    time1Parsed = datetime.strptime(time1, "%Y-%m-%d %H:%M:%S") # converts timestamp to datetime object
    time2Parsed = datetime.strptime(time2, "%Y-%m-%d %H:%M:%S")
    timeDiff = time2Parsed - time1Parsed
    return 86400 * timeDiff.days + timeDiff.seconds

def parse_line(line):
    if "Accelerometer:" in line:
        # Extract accelerometer data
        try:
            parts = line.split("Accelerometer: ")[1].split(" ")
            accel_data = list(map(float, parts[1::2])) # converts to list of floats
            accel_data.insert(0, "A") # adds ["A"] as first element to mark as accelerometer data
            return accel_data
        except Exception as e:
            print(e)
            pass
    elif "Gyroscope:" in line:
        # Extract gyroscope data
        try:
            parts = line.split("Gyroscope: ")[1].split(" ")
            gyro_data = list(map(float, parts[1::2]))
            gyro_data.insert(0, "G") # adds ["G"] as first element to mark as gyroscope data
            return gyro_data
        except Exception as e:
            print(e)
            pass
    else:
        # Attempt to parse as EMG value
        try:
            emg_value = float(line)
            return emg_value
        except Exception as e:
            print(e)
            pass

def compare(maxs, mins, num, i):
    if maxs[i] < num:
        maxs[i] = num
    if mins[i] > num:
        mins[i] = num

## plot data from csv file
def plotCSV(file):
    try:
        ## generate data from csv files
        dataframe = pd.read_csv(file)
        x1raw = dataframe["Timestamp"]
        # converts x axis into time elapsed in seconds
        x1 = []
        start_time = x1raw[0]
        for timestamp in x1raw:
            x1.append(timestampDiff(start_time, timestamp))
        y2raw = dataframe["Data"]

        dataList = [[],[],[],[],[],[],[]]
        timeList = [[],[],[]]
        maxList = [0,0,0,0,0,0,0] # used to set y lims - should be added to realtimeplot?
        minList = [0,0,0,0,0,0,0]

        for i in range(len(y2raw)):
            dataPoint = parse_line(y2raw[i])
            if type(dataPoint) == list: # Adds data to appropriate lists
                if dataPoint[0] == "A":
                    dataList[4].append(dataPoint[1])
                    compare(maxList, minList, dataPoint[1], 4)
                    dataList[5].append(dataPoint[2])
                    compare(maxList, minList, dataPoint[2], 5)
                    dataList[6].append(dataPoint[3])
                    compare(maxList, minList, dataPoint[3], 6)
                    timeList[2].append(x1[i])
                else:
                    dataList[1].append(dataPoint[1])
                    compare(maxList, minList, dataPoint[1], 1)
                    dataList[2].append(dataPoint[2])
                    compare(maxList, minList, dataPoint[2], 2)
                    dataList[3].append(dataPoint[3])
                    compare(maxList, minList, dataPoint[3], 3)
                    timeList[1].append(x1[i])
            elif type(dataPoint) == float:
                dataList[0].append(dataPoint)
                compare(maxList, minList, dataPoint, 0)
                timeList[0].append(x1[i])

        # adds subplots to container one at a time for uneven rows
        # indexes are numbered automatically from left to right, top-down
        fig = plt.figure(figsize=(10.0,6.0)) # size of the window in inches: width, height
        ax1 = fig.add_subplot(1, 3, 1) # args: nrows, ncols, index EMG
        ax2 = fig.add_subplot(3, 3, 2) # Gyro X
        ax3 = fig.add_subplot(3, 3, 5) # Gyro Y
        ax4 = fig.add_subplot(3, 3, 8) # Gyro Z
        ax5 = fig.add_subplot(3, 3, 3) # Accel X
        ax6 = fig.add_subplot(3, 3, 6) # Accel Y 
        ax7 = fig.add_subplot(3, 3, 9) # Accel Z

        # plots data
        ax1.plot(timeList[0], dataList[0])
        ax2.plot(timeList[1], dataList[1])
        ax3.plot(timeList[1], dataList[2])
        ax4.plot(timeList[1], dataList[3])
        ax5.plot(timeList[2], dataList[4])
        ax6.plot(timeList[2], dataList[5])
        ax7.plot(timeList[2], dataList[6])

        # axis formatting
        ax1.set_title("EMG")
        ax1.set_ylim([0, 1000])
        # ax1.set_ylabel("μV") # Need to check/add units
        # ax2.set_ylabel("°/s")
        ax2.set_title("Gyroscope")
        ax2.set_ylim([min(minList[1]-5000, -80000), max(maxList[1]+5000, 80000)]) # adjust y limits
        ax3.set_ylim([min(minList[2]-1000, -20000), max(maxList[2]+1000, 20000)])
        ax4.set_ylim([min(minList[3]-1000, -15000), max(maxList[3]+1000, 15000)])
        ax5.set_title("Accelerometer")
        ax5.set_ylim([min(minList[4]-50, -1050), max(maxList[4]+50, 1050)]) # adjust y limits
        ax6.set_ylim([min(minList[5]-50, -1050), max(maxList[5]+50, 1050)])
        ax7.set_ylim([min(minList[6]-50, -1050), max(maxList[6]+50, 1050)])
        ax5.set_ylabel("X")
        ax5.yaxis.set_label_position("right")
        ax6.set_ylabel("Y")
        ax6.yaxis.set_label_position("right")
        ax7.set_ylabel("Z")
        ax7.yaxis.set_label_position("right")

        # plt.savefig("file name") # uncomment to save as file
        plt.subplots_adjust(left=0.048, bottom=0.09, right=0.95, top=0.95, wspace=0.282, hspace=0.147) # formats the subplots, may need adjustment
        # plt.tight_layout() # alternate way to format subplots, doesn't seem to work well with these plots
        plt.show()
    except Exception as e:
        print(e)

plotCSV("C:/Users/tmsug/arduino_data_with_time5.csv")