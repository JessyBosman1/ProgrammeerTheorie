import csv
import os.path
import random
import itertools
import sys
sys.path.append("..")
import main
import time
starttime = time.time()

def bruteforce():
    """ Tries to fit every parcel in the parcellist into the spacecraft, 
        by calculating through the entire space.
    """
    spaceCraftId = main.createObjectsSpaceCraft()
    cargoListId = main.createObjectsCargoList()

    # Create all permutations of cargolist
    combinations = itertools.permutations(cargoListId.keys(), len(cargoListId.keys()))

    # Use counter to prematurely break loop to prevent a large amount of loops
    counter = 0

    # Used to remember last iteration, to skip the loop if the fitting parcels would be the same
    lastIteration = []
    packetCount = 1
    memorycount = 0

    print ('<<START LOOP>>')
    for combi in combinations:
        counter += 1
        if counter % 10000 == 0 and counter % 10000 != 0:
            print("Current loop number:", counter)

        # If the new list has the same packets in front as fitted in the one before, skip iteration
        # <! used for optimalisation >
        if list(combi)[:packetCount] == lastIteration[:packetCount]:
            continue
        lastIteration = list(combi)

        # Keep track of the number of parcels in the spaceCrafts
        packetCount = 0

        # Reset parameters of spacecraft / clear loading hold of spacecraft
        for spacecraft in spaceCraftId.keys():
            spaceCraftId[spacecraft].reset()

        for parcel in combi:
            # Try to fit every parcel into the spacecrafts
            for spacecraft in spaceCraftId.keys():
                if spaceCraftId[spacecraft].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
                    spaceCraftId[spacecraft].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
                    spaceCraftId[spacecraft].addParcelToParcellist(parcel)
                    packetCount += 1
                    break

        if packetCount > memorycount:
            memoryCount = packetCount
            print ('<<Info>>')
            for spacecraft in spaceCraftId.keys():
                print(spacecraft)
                print(len(spaceCraftId[spacecraft].parcellist), spaceCraftId[spacecraft].parcellist)
                print ("Payload (current, max)", spaceCraftId[spacecraft].currentPayload, spaceCraftId[spacecraft].maxPayload,
                   str(round(spaceCraftId[spacecraft].currentPayload / spaceCraftId[spacecraft].maxPayload * 100, 2)) + "%")
                print ("PayloadMass (current, max)", spaceCraftId[spacecraft].currentPayloadMass, spaceCraftId[spacecraft].maxPayloadMass, 
                   str(round(spaceCraftId[spacecraft].currentPayloadMass / spaceCraftId[spacecraft].maxPayloadMass * 100, 2)) + "%")
            endtime = time.time()
            print("Time: ", endtime - starttime, " seconds")
            print ('<<Total of '+ str(memoryCount) + ' parcels was found>>\n')

if __name__ == '__main__':
    bruteforce()

