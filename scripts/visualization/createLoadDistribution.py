
import csv
import os.path
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append("..")
import main

# create test loads
loadCygnus = ["CL1#80","CL1#64","CL1#92","CL1#29","CL1#4","CL1#74","CL1#71","CL1#81","CL1#56","CL1#59","CL1#79","CL1#90","CL1#9","CL1#52","CL1#49","CL1#94","CL1#15","CL1#6"]
loadProgress = ["CL1#48","CL1#77","CL1#78","CL1#43","CL1#96","CL1#18","CL1#67","CL1#68","CL1#40","CL1#76","CL1#28","CL1#100","CL1#3","CL1#98","CL1#37"]
loadKounotori = ["CL1#99","CL1#72","CL1#53","CL1#27","CL1#95","CL1#58","CL1#7","CL1#26","CL1#47","CL1#35","CL1#5","CL1#60","CL1#12","CL1#66","CL1#63",
             "CL1#2","CL1#1","CL1#62","CL1#41","CL1#45","CL1#70","CL1#55","CL1#91","CL1#65","CL1#97","CL1#85","CL1#87","CL1#75","CL1#42"]
loadDragon = ["CL1#17","CL1#25","CL1#51","CL1#73","CL1#24","CL1#14","CL1#36","CL1#13","CL1#88","CL1#32","CL1#46","CL1#21","CL1#89","CL1#10","CL1#19","CL1#54","CL1#8","CL1#11","CL1#69","CL1#20","CL1#16","CL1#23"]


def createPlotData(spacecraft, cargoList):
    """ Get data from load and base information from spacecraft to prepare plot data"""

    weightList = []
    volumeList = []

    totalWeight = 0
    totalVolume = 0

    maxWeightSpacecraft = main.spaceCraftId[spacecraft].maxPayloadMass
    maxVolumeSpacecraft = main.spaceCraftId[spacecraft].maxPayload

    for parcel in cargoList:
        # for each parcel add weight and volume to totalweight/volume
        totalWeight += main.cargoListId[parcel].weight
        weightList.append(totalWeight)

        totalVolume += main.cargoListId[parcel].volume
        volumeList.append(totalVolume)

    return weightList, volumeList, maxWeightSpacecraft, maxVolumeSpacecraft


def plotData(spacecraft, cargoList):
    # get data from createPlotData
    y,x, maxWeight, maxVolume = createPlotData(spacecraft, cargoList)

    # set max x and y limits to represent total dimensions of spacecraft
    plt.xlim(xmax = maxVolume, xmin = 0)
    plt.ylim(ymax = maxWeight, ymin = 0)

    # plot the bars
    plt.bar(x, y, color="#0f5fe0")

    # add titles
    plt.suptitle("distribution " + str(spacecraft), fontsize=18, fontweight='bold')
    plt.xlabel('volume (m^3)')
    plt.ylabel('weight (kg)')
    plt.title("(total of " + str(len(x)) + " parcels)", fontsize=12, style='italic')

    # show the plot
    plt.show()

plotData("Cygnus",loadCygnus)
plotData("Progress",loadProgress)
plotData("Kounotori",loadKounotori)
plotData("Dragon",loadDragon)
