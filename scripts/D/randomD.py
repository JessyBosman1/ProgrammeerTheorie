import csv
import os.path
import random
import itertools
import sys
sys.path.append("..")
import main
from random import shuffle
import time
starttime = time.time()

memoryCount = 77

def randomHelper():
    # Prepare the spacecraft and cargolist
    spacecraftobject = main.createObjectsSpaceCraft("DE")
    cargoobject = main.createObjectsCargoList(3)

    # Make a list with the different spacecrafts
    spacecrafts = [spacecraft for spacecraft in spacecraftobject.keys()]

    # Create a random order of parcels
    parcels = [parcel for parcel in cargoobject.keys()]
    return spacecraftobject, cargoobject, spacecrafts, parcels

def randomAlgorithmD(numberofloops):
    bestattemptdict = {}
    bestattemptprice = 1000000000000000000000000000000000000000000000
    spaceCraftId, cargoListId, spacecraftList, parcelList = randomHelper()
    for loop in range(numberofloops):
        # Print loop every now and then to keep user updated
        if loop % 10000 == 0 and loop % 10000 != 0:
            print("Current loop number:", loop)

        # Randomize the order in de parcellist
        parcelList = [parcel for parcel in cargoListId.keys()]
        random.shuffle(parcelList)

        results = {}
        counter = 0
        totalprice = 0
        parcelcheck = 1250
        for i in range(0,100):
            counter = i
            if len(parcelList) != 0:
                runresult, runlist, runprice = fillSpacecrafts(parcelList, spaceCraftId, cargoListId, spacecraftList)
                results[counter] =  runresult
                parcelList = runlist
                totalprice += runprice
        print(totalprice, len(results.keys()))
        if totalprice < bestattemptprice:
            bestattemptprice = totalprice
            bestattemptdict = results
            print ("<<<< NEW BEST, ", totalprice, " DOLLARS WHILE FLYING ", len(bestattemptdict.keys()), " TIMES >>>>")
    print ("<<<< BEST FOUND, ", totalprice, " DOLLARS WHILE FLYING ", len(bestattemptdict.keys()), " TIMES >>>>")
    testlijst = []
    
    """ Testje om te checken als er iets aangepast wordt
    for k,v in results.items():
        for x,y in v.items():
            if x == "Parcellists":
                for a,b in y.items():
                    for item in b:
                        testlijst.append(item)
    print(testlijst, len(testlijst))"""

def fillSpacecrafts(parcelList, spaceCraftId, cargoListId, spacecraftList):
    # Create a copy of the parcellist, because you don't want to loop
    # through a list while you are removing items from that list
    copyparcel = [x for x in parcelList]
    
    # Reset spacecrafts
    for spacecraft in spaceCraftId.keys():
        spaceCraftId[spacecraft].reset()

    # Reset the parcellists and packetcount
    space0 = []
    space1 = []
    space2 = []
    space3 = []
    space4 = []
    space5 = []
    packetCount = 0

    # Fill the spacecrafts
    for parcel in copyparcel:
        parcelList.remove(parcel)
        if spaceCraftId[spacecraftList[0]].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
            spaceCraftId[spacecraftList[0]].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
            space0.append(parcel)
            packetCount += 1
        elif spaceCraftId[spacecraftList[1]].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
            spaceCraftId[spacecraftList[1]].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
            space1.append(parcel)
            packetCount += 1
        elif spaceCraftId[spacecraftList[2]].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
            spaceCraftId[spacecraftList[2]].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
            space2.append(parcel)
            packetCount += 1
        elif spaceCraftId[spacecraftList[3]].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
            spaceCraftId[spacecraftList[3]].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
            space3.append(parcel)
            packetCount += 1
        elif spaceCraftId[spacecraftList[4]].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
            spaceCraftId[spacecraftList[4]].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
            space4.append(parcel)
            packetCount += 1
        elif spaceCraftId[spacecraftList[5]].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
            spaceCraftId[spacecraftList[5]].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
            space5.append(parcel)
            packetCount += 1
        else:
            parcelList.append(parcel)
            break

    parceldict = {spacecraftList[0]:space0, spacecraftList[1]:space1, spacecraftList[2]:space2, spacecraftList[3]:space3, spacecraftList[4]:space4, spacecraftList[5]:space5}
    aantalparcels = {spacecraftList[0]:len(space0), spacecraftList[1]:len(space1), spacecraftList[2]:len(space2), spacecraftList[3]:len(space3), spacecraftList[4]:len(space4), spacecraftList[5]:len(space5)}
    weight = {}
    volume = {}
    price = {}
    runprice = 0
    for spacecraft in spaceCraftId.keys():
        weight[spacecraft] = spaceCraftId[spacecraft].currentPayloadMass
        volume[spacecraft] = spaceCraftId[spacecraft].currentPayload
        ftw = spaceCraftId[spacecraft].fuelToWeight
        price[spacecraft] = spaceCraftId[spacecraft].calculateFuel(ftw) + spaceCraftId[spacecraft].baseCost
        runprice += spaceCraftId[spacecraft].calculateFuel(ftw) + spaceCraftId[spacecraft].baseCost
    returndict = {"Parcellists":parceldict, "NumberOfParcels":aantalparcels, "weight":weight, "volume":volume, "price":price}
    return returndict, parcelList, runprice
randomAlgorithmD(1500);
