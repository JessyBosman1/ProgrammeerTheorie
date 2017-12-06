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

def randomAlgorithm(numberofloops, stopnumber=97):
    """ Function that fills the spacecrafts randomly.
        Input: numberofloops, the total number of attempts
               stopnumber, function returns highest when this number
                           is reached
    """

    # Get the spacecraft and cargolist objects from main.py
    spaceCraftId = main.createObjectsSpaceCraft()
    cargoListId = main.createObjectsCargoList()

    # Create all the different orders of spacecrafts
    spaceList = ['Progress', 'Cygnus', 'Kounotori', 'Dragon']
    shuffleGen = itertools.permutations(spaceList, len(spaceList))
    shuffleList = [x for x in shuffleGen]

    # Initialize a variable that keeps track of the largest number of parcels
    memoryCount = 77

    # Create an random order of parcels
    randomList = [x for x in range(1,101)]

    # Remove the heaviest parcels
    randomList.remove(83)
    randomList.remove(58)
    randomList.remove(34)

    for loop in range(numberofloops):
        # Print the number of runs every 240000
        if loop % 10000 == 0 and loop % 10000 != 0:
            print("Current loop number:", loop * len(shuffleList))

        # Shuffle the parcel order every loop
        random.shuffle(randomList)

        # Loop through all the different orders that the spacecrafts can be in
        for spacer in shuffleList:

            # "Empty" the spacecrafts and reset counter
            spaceCraftId['Progress'].reset()
            spaceCraftId['Cygnus'].reset()
            spaceCraftId['Kounotori'].reset()
            spaceCraftId['Dragon'].reset()
            packetCount = 0
            space0 = []
            space1 = []
            space2 = []
            space3 = []

            # Try to fit every parcel in a spacecraft
            for i in randomList:
                parcel = 'CL1#' + str(i)

                # If there is room in the spacecraft, add the parcel
                if spaceCraftId[spacer[0]].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
                    spaceCraftId[spacer[0]].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
                    space0.append(parcel)
                    packetCount += 1

                elif spaceCraftId[spacer[1]].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
                    spaceCraftId[spacer[1]].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
                    space1.append(parcel)
                    packetCount += 1

                elif spaceCraftId[spacer[2]].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
                    spaceCraftId[spacer[2]].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
                    space2.append(parcel)
                    packetCount += 1

                elif spaceCraftId[spacer[3]].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
                    spaceCraftId[spacer[3]].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
                    space3.append(parcel)
                    packetCount += 1

            # Only print the result when there are more than 78 parcels in the spacecrafts
            if packetCount > memoryCount:
                print ('<<Info>>')
                print (packetCount)
                print (spacer[0], space0)
                print ('---------------')
                print (spacer[1], space1)
                print ('---------------')
                print (spacer[2], space2)
                print ('---------------')
                print (spacer[3], space3)
                print ('---------------')
                print (spacer[0], len(space0), spacer[1], len(space1), spacer[2], len(space2), spacer[3], len(space3), "\n")

                for y in spaceCraftId.keys():
                    print(y)
                    print ("Payload (current, max)", spaceCraftId[y].currentPayload, spaceCraftId[y].maxPayload,
                       str(round(spaceCraftId[y].currentPayload / spaceCraftId[y].maxPayload * 100, 2)) + "%")
                    print ("PayloadMass (current, max)", spaceCraftId[y].currentPayloadMass, spaceCraftId[y].maxPayloadMass, 
                       str(round(spaceCraftId[y].currentPayloadMass / spaceCraftId[y].maxPayloadMass * 100, 2)) + "%")

                endtime = time.time()
                print("Tijd: ", endtime - starttime)

            
            if packetCount == stopnumber or packetCount > stopnumber:
                return spacer[0], space0, spacer[1], space1, spacer[2], space2, spacer[3], space3, spaceCraftId
        # Keep track of the highest parcelcount
        if packetCount > memoryCount:
            memoryCount = packetCount
            print(memoryCount)

