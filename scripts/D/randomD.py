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
    """ Generates the spacraft class and cargolist class 
    """

    # Prepare the spacecraft and cargolist
    spacecraftobject = main.createObjectsSpaceCraft("DE")
    cargoobject = main.createObjectsCargoList(3)

    # Make a list with the different spacecrafts
    spacecrafts = [spacecraft for spacecraft in spacecraftobject.keys()]

    # Create a random order of parcels
    parcels = [parcel for parcel in cargoobject.keys()]
    return spacecraftobject, cargoobject, spacecrafts, parcels

def randomAlgorithmD(numberofloops):
    """ Tries to solve problem D, by fitting as many parcels in a load,
        resetting the crafts and them fills the next load etc. untill
        all the parcels are in a spaceship
    """
    # Set an unrealisticly high price as cheapest price, so cheaper attempts can be found
    bestattemptdict = {}
    bestattemptprice = 1000000000000000000000000000000000000000000000
    spaceCraftId, cargoListId, spacecraftList, parcelList = randomHelper()

    for loop in range(numberofloops):
        # Print loop every now and then to keep user updated
        if loop % 100 == 0 and loop % 1000 != 0:
            print("Current loop number:", loop, "Best totalprice = ", bestattemptprice, " while flying ", len(bestattemptdict.keys()), " times" )

        # Randomize the order in de parcellist
        parcelList = [parcel for parcel in cargoListId.keys()]
        random.shuffle(parcelList)

        results = {}
        counter = 0
        totalprice = 0

        # We know that every ship can take at least 10 packets, so the maximum
        # amount of loads is 1250/10/6 = 21, so try to fill a load 22 times
        for i in range(0,22):
            counter = i

            if len(parcelList) != 0:
                # Try to fill the spacecraft and save the results for
                # future referencing
                runresult, runlist, runprice = fillSpacecrafts(parcelList, spaceCraftId, cargoListId, spacecraftList)
                results[counter] =  runresult
                parcelList = runlist
                totalprice += runprice
        
        if totalprice < bestattemptprice:
            bestattemptprice = totalprice
            bestattemptdict = results
            print ("<<<< NEW BEST, ", totalprice, " DOLLARS WHILE FLYING ", len(bestattemptdict.keys()), " TIMES >>>>")

    print ("<<<< BEST FOUND, ", totalprice, " DOLLARS WHILE FLYING ", len(bestattemptdict.keys()), " TIMES >>>>")


def fillSpacecrafts(parcelList, spaceCraftId, cargoListId, spacecraftList):
    """ Fills the spacecrafts by trying to fit as many parcels as possible
    """
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
        # Loop through all the spacecrafts and see it the parcel fits, if it does, add it
        for spacecraft in spaceCraftId.keys():
            if spaceCraftId[spacecraft].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
                spaceCraftId[spacecraft].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
                spaceCraftId[spacecraft].addParcelToParcellist(parcel)
                parcelList.remove(parcel)
                packetCount += 1
                break

    # Gather all the information to return
    parceldict = {}
    aantalparcels = {}
    weight = {}
    volume = {}
    price = {}
    runprice = 0

    for spacecraft in spaceCraftId.keys():
        parceldict[spacecraft] = spaceCraftId[spacecraft].parcellist
        aantalparcels[spacecraft] = len(spaceCraftId[spacecraft].parcellist)
        weight[spacecraft] = spaceCraftId[spacecraft].currentPayloadMass
        volume[spacecraft] = spaceCraftId[spacecraft].currentPayload

        ftw = spaceCraftId[spacecraft].fuelToWeight
        if spaceCraftId[spacecraft].currentPayloadMass != 0 and spaceCraftId[spacecraft].currentPayload != 0:
            price[spacecraft] =  spaceCraftId[spacecraft].calculateCost(spaceCraftId[spacecraft].calculateFuel())
            runprice += spaceCraftId[spacecraft].calculateCost(spaceCraftId[spacecraft].calculateFuel())
        else:
            price[spacecraft] = 0
            runprice += 0

    # Create the dict that will be returned
    returndict = {"Parcellists":parceldict, "NumberOfParcels":aantalparcels, "weight":weight, "volume":volume, "price":price}
    return returndict, parcelList, runprice

if __name__ == '__main__':
    randomAlgorithmD(10000000);
