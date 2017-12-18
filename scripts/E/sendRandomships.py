import csv
import os.path
import random
import itertools
import sys
sys.path.append("..")
sys.path.append("../D")
import main
import randomD
from random import shuffle
import time

def randomspacecraftfiller(numberofloops):
    """ Triest to fill one spacecraft at the time to make a completely random  
        fleet that sends all the 1250 parcels
    """
    # Prepare spacecrafts an cargolist
    spaceCraftId, cargoListId, spacecraftList, parcelList = randomD.randomHelper()
    results = {}
    counter = 0

    # Set an unrealisticly high price as cheapest price, so cheaper attempts can be found
    bestattemptdict = {}
    bestattemptprice = 1000000000000000000000000000000000000000000000

    for loop in range(numberofloops):
        parcelList = [parcel for parcel in cargoListId.keys()]
        totalprice = 0
        counter += 1
        run = {}
        attemptdict = {}

        # Keep track of if all the 1250 parcels are in the fleet
        done = False
        while done != True:
            if len(parcelList) != 0:
                # Get a random ship
                random.shuffle(parcelList)
                ship = random.choice(spacecraftList)

                # Fill the random chosen ship
                parcelList, runsummary = fillship(ship, parcelList, spaceCraftId, cargoListId)
                totalprice += runsummary["Price"]

                # Add the ship to the dict with the other ships in the fleet
                attemptdict[str(ship) + str(time.time())] = runsummary

            else:
                # If the parcellist is empty, add the complete fleet to the dict  with runs
                run[counter] = attemptdict
                done = True
        results[counter] = run

        # Update the information about the best attempt when needed
        if totalprice < bestattemptprice:
            bestattemptprice = totalprice
            bestattemptdict = run
            runs = 0
            for k,v in run.items():
                runs = len(v.keys())


            print ("<<<< NEW BEST, ", totalprice, " DOLLARS WHILE FLYING ", runs, " TIMES >>>>")
    return bestattemptdict, bestattemptprice


def fillship(namespaceship, parcellist, spaceCraftId, cargoListId):
    """ Tries to fill the ships randomly
    """
    # Create a copy of the parcellist, because you don't want to loop
    # through a list while you are removing items from that list
    copyparcel = [x for x in parcellist]

    # Reset the spacecraft incase it was used in a previous fill
    spaceCraftId[namespaceship].reset()
    parcelsinship = []
    packetCount = 0
    parcelsreminder = []

    for parcel in copyparcel:
        parcellist.remove(parcel)
        # Loop through all the spacecrafts and see it the parcel fits, if it does, add it
        if spaceCraftId[namespaceship].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
            spaceCraftId[namespaceship].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
            parcelsinship.append(parcel)
            packetCount += 1
        else:
            parcelsreminder.append(parcel)

    price =  spaceCraftId[namespaceship].calculateCost(spaceCraftId[namespaceship].calculateFuel())
    returndict = {"Parcels":parcelsinship, "NumberParcel":len(parcelsinship),
                  "Weight":spaceCraftId[namespaceship].currentPayloadMass,
                  "volume":spaceCraftId[namespaceship].currentPayload, "Price":price}
    return parcelsreminder, returndict


def printresult(returndict, totalprice):
    for k,v in returndict.items():
        runs = [x for x,y in v.items()]
    totalruns = len(runs)
    print("<<< Cheapest run found was $", totalprice, "where ", totalruns, " spacecrafts were send. >>>")
    print("The following spacecrafts were send:", runs)


if __name__ == '__main__':
    returndict, totalprice = randomspacecraftfiller(500)
    printresult(returndict, totalprice)


