import os.path
import random
import itertools
import sys
sys.path.append("..")
import main
from random import shuffle
import time


def randomAlgorithm(numberofloops, stopnumber=97, memorycount=77, parcellist=1):
    """ Function that fills the spacecrafts randomly.
        Input: numberofloops, the total number of attempts
               stopnumber, function returns highest attempt when 
                           this number of packets is reached
        Output: highest attempt found
    """
    starttime = time.time()
    # Get the spacecraft and cargolist objects from main.py
    spaceCraftId = main.createObjectsSpaceCraft()
    cargoListId = main.createObjectsCargoList(parcellist)

    # Create all the different orders of spacecrafts
    spaceList = [spacecraft for spacecraft in spaceCraftId.keys()]
    shuffleGen = itertools.permutations(spaceList, len(spaceList))
    shuffleList = [x for x in shuffleGen]

    # Initialize a variable that keeps track of the largest number of parcels
    memoryCount = memorycount

    # Create an random order of parcels
    randomList = [parcel for parcel in cargoListId.keys()]

    for loop in range(numberofloops):
        # Print the number of runs every 240000
        if loop % 1000 == 0 and loop % 5000 != 0:
            print("Current loop number:", loop * len(shuffleList))

        # Shuffle the parcel order every loop
        random.shuffle(randomList)

        # Loop through all the different orders that the spacecrafts can be in
        for spacer in shuffleList:

            # "Empty" the spacecrafts and reset counter
            for spacecraft in spaceList:
                spaceCraftId[spacecraft].reset()
            packetCount = 0

            # Try to fit every parcel in a spacecraft
            for parcel in randomList:
                for spacecraft in spacer:
                    if spaceCraftId[spacecraft].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
                        spaceCraftId[spacecraft].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
                        spaceCraftId[spacecraft].addParcelToParcellist(parcel)
                        packetCount += 1
                        break

            # Only print the result when there are more than 78 parcels in the spacecrafts
            if packetCount > memoryCount:
                memoryCount = packetCount
                print ('<<Info>>')
                for spacecraft in spaceList:
                    print(spacecraft)
                    print(len(spaceCraftId[spacecraft].parcellist), spaceCraftId[spacecraft].parcellist)
                    print ("Payload (current, max)", spaceCraftId[spacecraft].currentPayload, spaceCraftId[spacecraft].maxPayload,
                       str(round(spaceCraftId[spacecraft].currentPayload / spaceCraftId[spacecraft].maxPayload * 100, 2)) + "%")
                    print ("PayloadMass (current, max)", spaceCraftId[spacecraft].currentPayloadMass, spaceCraftId[spacecraft].maxPayloadMass, 
                       str(round(spaceCraftId[spacecraft].currentPayloadMass / spaceCraftId[spacecraft].maxPayloadMass * 100, 2)) + "%")
                endtime = time.time()
                print("Time: ", endtime - starttime, " seconds")
                print ('<<Total of '+ str(memoryCount) + ' parcels was found>>\n')

            if packetCount >= stopnumber:
                return spaceCraftId

    return spaceCraftId

if __name__ == '__main__':
    randomAlgorithm(100000, 97, 77, 1)

