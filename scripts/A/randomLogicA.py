import csv
import os.path
import random
import itertools
import sys
sys.path.append("..")
import main
import randomA
from random import shuffle
import time

def randomLogicA (numberofloops, numberofloopsRandom):
    """ Function that empties the spacrafts Cygnus and Dragon and tries
        to fit more parcels in total into the four spacecrafts.
        Input: numberofLoops, number of loops that the function tries to 
                              refill Cynus and Dragon
               numberofLoopsRandom, number of loops that the random is runned 
                                    before trying to refill the spacrafts
    """
    starttime = time.time()
    cargoListId = main.createObjectsCargoList()

    # Get the output from RandomA
    spaceCraftId = randomA.randomAlgorithm(round(numberofloopsRandom/24), 78)

    # Get all the parcels
    parcelList = [x for x in cargoListId.keys()]
    parcelList.remove("CL1#83")
    parcelList.remove("CL1#58")
    parcelList.remove("CL1#34")
    start = len(parcelList)

    # Empty the spacecrafts Cygnus and Dragon and reset them
    alreadyin = 0
    correction = 0
    for spacecraft in spaceCraftId.keys():
        if spaceCraftId[spacecraft].spacecraft == "Cygnus" or spaceCraftId[spacecraft].spacecraft == "Dragon":
            correction += len(spaceCraftId[spacecraft].parcellist)
            spaceCraftId[spacecraft].reset()
        else:
            # Remove the parcels from Kounotori and Progress from the parcellist
            # because the spacecrafts already have those parcels in it
            alreadyin += len(spaceCraftId[spacecraft].parcellist)
            parcelList = set(parcelList) - set(spaceCraftId[spacecraft].parcellist)

    # Convert the parcellist from a set to a list again
    parcelList = list(parcelList)

    # Create new random shuffle for the two spacecrafts
    spaceList = ["Cygnus", "Dragon"]
    shuffleGen = itertools.permutations(spaceList, len(spaceList))
    shuffleList = [x for x in shuffleGen]

    # Make the highest parcelcount the memory count
    memorycount = 78

    print("<<START SECOND LOOP>>")
    for loop in range(numberofloops):

        # Print the loop number now and then for the user
        if loop % 50000 == 0:
            print("Current loop number:", loop)

        # Shuffle the parcels and set the packetcount
        random.shuffle(parcelList)
        packetCount =  alreadyin

        for spacer in shuffleList:
            # Reset parameters of spacecraft / clear loading hold of spacecraft
            spaceCraftId['Cygnus'].reset()
            spaceCraftId['Dragon'].reset()
            packetCount = alreadyin

            # Try to fit every parcel in a spacecraft
            for parcel in parcelList:
                for spacecraft in spacer:
                    if spaceCraftId[spacecraft].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
                        spaceCraftId[spacecraft].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
                        spaceCraftId[spacecraft].addParcelToParcellist(parcel)
                        packetCount += 1
                        break

            # If the packet count is higher than the memory count, let the user know
            if packetCount > memorycount:
                memorycount = packetCount
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
                print ('<<Total of '+ str(memorycount) + ' parcels was found>>\n')

    return memorycount

if __name__ == '__main__':
    randomLogicA(400000, 300000)
