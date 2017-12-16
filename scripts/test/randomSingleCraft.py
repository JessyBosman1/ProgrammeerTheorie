import random
import itertools
import os
import sys
sys.path.append("..")
import main
import csv

def randomSingleCraft(craftName, craftListN, cargoListN):
    """"
    systematically fill one spacecraft multiple times until
    there are no more parcels left.
    """
    # get correct spacecraft and cargo IDs.
    spaceCraftId = main.createObjectsSpaceCraft(craftListN)
    cargoListId = main.createObjectsCargoList(cargoListN)

    # get requested parcelList
    parcelList = [parcel for parcel in cargoListId.keys()]

    # Controlvariable, keeps track of total packets,
    # should be equal to length of cargolist when done
    packetCountTotal = 0

    nTrips = 0
    totalPrice = 0

    while parcelList != []:
        # clear spacecraft to simulate next trip
        spaceCraftId[craftName].reset()
        SpacecraftStorage = []
        packetCountCurrent = 0
        nTrips = nTrips + 1

        # create the remainingParcels to loop through
        remainingParcels = [x for x in parcelList]

        for parcel in remainingParcels:
            # Check if the parcels fits in the craft, if true, add.
            if spaceCraftId[craftName].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
                spaceCraftId[craftName].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
                # remove from remaining parcels, and add to storage.
                SpacecraftStorage.append(parcel)
                parcelList.remove(parcel)
                # update counters
                packetCountCurrent += 1
                packetCountTotal += 1

        totalPrice = totalPrice + spaceCraftId[craftName].calculateCost(spaceCraftId[craftName].calculateFuel())

        #parcelList = []

        print ("currentTripLoad: " + str(SpacecraftStorage))
        print ("currentTripNumber: " + str(nTrips))
        print ("currentTripAmount: " + str(packetCountCurrent))
        print ("totalprice: " + str(totalPrice))

if __name__ == "__main__":
    randomSingleCraft('Dragon', "DE", 3)
    
#25893000000.0   << TianZhou
#39022500000.0   << Verne ATV
#56715316550.0   << Cygnus
#26417208000.0   << Progress
#30429745650.0   << Kounotori
#35816895950.0   << Dragon
