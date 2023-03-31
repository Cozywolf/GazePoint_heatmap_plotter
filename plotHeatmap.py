# %% Block 1: Creaking folder structure
import os
if not os.path.exists('./data/'):
    os.mkdir('./data/')
if not os.path.exists('./bg/'):
    os.mkdir('./bg/')
if not os.path.exists('./plots/'):
    os.mkdir('./plots/')
if not os.path.exists('./plots/perSubject/'):
    os.mkdir('./plots/perSubject/')
if not os.path.exists('./plots/overall/'):
    os.mkdir('./plots/overall/')

# %% Block 2: REQUIRED INFO
# This should be the only section that you need to modify, please review each comment carefully and modify as needed.
# Participant number, e.g., ['P001', 'P002', 'P003']
pp = ['P001', 'P002', 'P003']

# You can specify where the data files are located but it is recommended to copy your data files into where this script/data folder
# The folder should contain ONLY data csv files and the data file must be named in the format <Participant number>_fixations.csv
# e.g., 'P001_fixations.csv'
dataPath = './data/'

# Event timestamp file, see exampleTimestamp.csv for reference, it must be formatted in the exact way and place at the same level as this script
# Event time should be in Unix time (10 digits) and can have decimals, if you use nanosecond device it by 1,000,000
timestampFile = 'exampleTimestamp.csv'

# plot out directory
outputPath = './plots/perSubject/'
# plot out directory
overalloutputPath = './plots/overall/'

# Screen resolution, beaware that some of the bigger display might be in higher resolution like 2560x1440 or 3840x2160
display_width = 1920
display_height = 1080

# Plotting mode, 1 = shared background image, 2 = individual images, 3 = no image (export transparent png for overlaying)
bgOption = 2
# If you select 1 (shared background image) please specify background image, should be in .png
background_image = './bg/<shared image name>.png'
# If you select 2 (individual images) please specify the path to images, the images show has be named as "participantNumber_condition.png" that matches the event timestamp file, for instance "P001_Single_1.png"
backgroundImgPath = './bg/'

# plotting parameters, if you are not sure what they are can just leave them as default
alpha = 0.5 # Alpha level (0 - 1)
ngaussian = 200 # Gaussian matrix
sd = 33 # standard deviation

# %% Block 3: import modules and functions
import pandas as pd
from matplotlib import pyplot, image
import time
from datetime import datetime
import numpy
import heatmap

def reformatData(fullPath, x, y):
    df = pd.read_csv(fullPath)
    df.columns[df.columns.str.startswith("TIME(")]
    name = df.columns[df.columns.str.startswith("TIME(")]
    # print(name[0][5:-1])
    dt_obj = datetime.strptime(name[0][5:-1],'%Y/%m/%d %H:%M:%S.%f')
    startTime = time.mktime(dt_obj.timetuple()) + dt_obj.microsecond/1000000
    # print(dt_obj)
    # print(time.mktime(dt_obj.timetuple()) + dt_obj.microsecond/1000000)
    df['UnixTime'] = df[name[0]] + startTime
    df['FPOGX'] = df['FPOGX']*x
    df['FPOGY'] = df['FPOGY']*y
    df['FPOGD'] = df['FPOGD']*1000
    return (df)

def plotHeadmap(gaze_data, output_name, background_image):
    heatmap.draw_heatmap(gaze_data, (display_width, display_height), alpha=alpha, savefilename=output_name, imagefile=background_image, gaussianwh=ngaussian, gaussiansd=sd)


# %% Block 4: Load event timestamps
timeStamps = pd.read_csv(timestampFile)
conditionCount = int(len(timeStamps['events'])/2)
timeStamps.head()


# %% Block 5: Load all data files and plot heatmaps
dataSets = {}
combinedData = {}

for sub in pp:
    fullPath = dataPath + "{}_fixations.csv".format(sub)
    dataSets[sub] = reformatData(fullPath, display_width, display_height)
    for condition in range(conditionCount):
        eventName = timeStamps['events'][condition*2][:-6]
        print(eventName)
        start = timeStamps[sub][condition*2]
        end = timeStamps[sub][condition*2 + 1]
        subDataSet = dataSets[sub][dataSets[sub]["UnixTime"].between(start,end)]
        outputName = outputPath + sub + "_" + eventName + '.png' 
        print(sub, eventName, "Total fixations = ", subDataSet.shape[0])
        if bgOption == 1:
            bgname = background_image
        elif bgOption == 2:
            bgname = backgroundImgPath + eventName + '.png'
        elif bgOption == 3:
            bgname = None
        plotHeadmap(list(zip(subDataSet['FPOGX'], subDataSet['FPOGY'], subDataSet['FPOGD'])), outputName, bgname)
        
        if eventName in combinedData.keys():
            combinedData[eventName] = pd.concat([combinedData[eventName], subDataSet], axis=0)
        else:
            combinedData[eventName] = subDataSet
        
        # print(eventName, combinedData[eventName].shape)

for key in combinedData:
    if bgOption == 1:
        bgname = background_image
    elif bgOption == 2:
        bgname = backgroundImgPath + key + '.png'
    elif bgOption == 3:
        bgname = None
    outputName = overalloutputPath + key + '_all.png'
    plotHeadmap(list(zip(combinedData[key]['FPOGX'], combinedData[key]['FPOGY'], combinedData[key]['FPOGD'])), outputName, bgname)