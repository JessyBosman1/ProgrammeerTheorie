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

def randomLogicA (numberofloops):
    starttime = time.time()
    cargoListId = main.createObjectsCargoList()

    # Get the output from RandomA
    a, ax, b, bx, c, cx, d, dx, spaceCraftId = randomA.randomAlgorithm(100000, 78)
    spaceshiplist = [a, b, c, d]
    start = len(ax+bx+cx+dx)

    # Get all the used parcels
    parcelList = []
    for x in cargoListId.keys():
        parcelList.append(x)
    parcelList.remove("CL1#83")
    parcelList.remove("CL1#58")
    parcelList.remove("CL1#34")

    # Empty the spacecrafts Cygnus and Dragon
    correction = 0
    if a == "Cygnus":
        correction += len(ax)
        spaceCraftId['Cygnus'].reset()
        spaceshiplist.remove(a)
        ax = []
    elif b == "Cygnus":
        correction += len(bx)
        spaceCraftId['Cygnus'].reset()
        spaceshiplist.remove(b)
        bx = []
    elif c == "Cygnus":
        correction += len(cx)
        spaceCraftId['Cygnus'].reset()
        spaceshiplist.remove(c)
        cx = []
    elif d == "Cygnus":
        correction += len(dx)
        spaceCraftId['Cygnus'].reset()
        spaceshiplist.remove(d)
        dx = []

    if a == "Dragon":
        correction += len(ax)
        spaceCraftId['Dragon'].reset()
        spaceshiplist.remove(a)
        ax = []
    elif b == "Dragon":
        correction += len(bx)
        spaceCraftId['Dragon'].reset()
        spaceshiplist.remove(b)
        bx = []
    elif c == "Dragon":
        correction += len(cx)
        spaceCraftId['Dragon'].reset()
        spaceshiplist.remove(c)
        cx = []
    elif d == "Dragon":
        correction += len(dx)
        spaceCraftId['Dragon'].reset()
        spaceshiplist.remove(d)
        dx = []

    # Create new random shuffle
    spaceList = ['Cygnus', 'Dragon']
    shuffleGen = itertools.permutations(spaceList, len(spaceList))
    shuffleList = [x for x in shuffleGen]

    # Remove the parcels from the other 2 spacecrafts from
    # the list with all of the parcels
    for parcel in ax:
        parcelList.remove(parcel)
    for parcel in bx:
        parcelList.remove(parcel)
    for parcel in cx:
        parcelList.remove(parcel)
    for parcel in dx:
        parcelList.remove(parcel)

    # Make the highest parcelnumber so far the memory count
    memorycount = 78
    print("<<START SECOND LOOP>>")
    for loop in range(numberofloops):
        if loop % 50000 == 0:
            print("Current loop number:", loop)

        random.shuffle(parcelList)

        packetCount = start - correction

        # Reset parameters of spacecraft / clear loading hold of spacecraft
        for spacer in shuffleList:
            spaceCraftId['Cygnus'].reset()
            spaceCraftId['Dragon'].reset()
            packetCount = start - correction

            #print (start, len(parcelList), packetCount)


            space0 = []
            space1 = []

            # Try to fit every parcel in a spacecraft
            for i in parcelList:
                parcel = str(i)

                # If there is room in the spacecraft, add the parcel
                if spaceCraftId[spacer[0]].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
                    spaceCraftId[spacer[0]].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
                    space0.append(parcel)
                    packetCount += 1
                elif spaceCraftId[spacer[1]].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
                    spaceCraftId[spacer[1]].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
                    space1.append(parcel)
                    packetCount += 1

            #print (packetCount)
            if packetCount > memorycount:
                memorycount = packetCount
                print ('<<Details>>')
                print (spacer[0], space0)
                print ('---------------')
                print (spacer[1], space1)
                print ('---------------')
                for y in spaceCraftId.keys():
                    print(y)
                    print ("Payload (current, max)", spaceCraftId[y].currentPayload, spaceCraftId[y].maxPayload,
                       str(round(spaceCraftId[y].currentPayload / spaceCraftId[y].maxPayload * 100, 2)) + "%")
                    print ("PayloadMass (current, max)", spaceCraftId[y].currentPayloadMass, spaceCraftId[y].maxPayloadMass, 
                       str(round(spaceCraftId[y].currentPayloadMass / spaceCraftId[y].maxPayloadMass * 100, 2)) + "%")
                print (spacer[0], len(space0), spacer[1], len(space1))#,"Progress", len(Progress), "Kounotori", len(Kounotori), "\n")
                print ("Total: ", packetCount)
                endtime = time.time()
                print("Tijd: ", endtime - starttime)

if __name__ == '__main__':
    randomLogicA(100000)
