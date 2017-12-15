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
    spaceCraftId = main.createObjectsSpaceCraft()
    cargoListId = main.createObjectsCargoList()

    # little check to see the total parcel weight and volume
    print ('<<TOTAL LOAD>>')
    totalWeight = 0
    totalVolume = 0
    for parcel in cargoListId.keys():
        totalWeight = totalWeight + cargoListId[parcel].weight
        totalVolume = totalVolume + cargoListId[parcel].volume
    print ("Total weight: ", totalWeight)
    print ("Total volume: ", totalVolume)


    # create all permutations of cargolist
    combinations = itertools.permutations(cargoListId.keys(), len(cargoListId.keys()))

    # use counter to prematurely break loop to prevent a large amount of loops
    counter = 0
    # used to remember last iteration, to skip the loop if the fitting parcels would be the same
    lastIteration = []
    packetCount = 1
    memorycount = 0

    print ('<<START LOOP>>')
    for combi in combinations:
        counter += 1
        if counter % 10000 == 0 and counter % 10000 != 0:
            print("Current loop number:", counter)

        # if the new list has the same packets in front as fitted in the one before, skip iteration
        # <! used for optimalisation >
        if list(combi)[:packetCount] == lastIteration[:packetCount]:
            continue
        lastIteration = list(combi)

        # keep track of the number of parcels in the spaceCrafts
        packetCount = 0

        # reset parameters of spacecraft / clear loading hold of spacecraft
        spaceCraftId['Progress'].reset()
        spaceCraftId['Cygnus'].reset()
        spaceCraftId['Kounotori'].reset()
        spaceCraftId['Dragon'].reset()
        Progress = []
        Cygnus = []
        Kounotori = []
        Dragon = []

        # for every parcel in combination
        for parcel in combi:
            # if there is room: add
            if spaceCraftId['Progress'].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
                spaceCraftId['Progress'].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
                Progress.append(parcel)
                packetCount += 1
            elif spaceCraftId['Cygnus'].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
                spaceCraftId['Cygnus'].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
                Cygnus.append(parcel)
                packetCount += 1
            elif spaceCraftId['Kounotori'].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
                spaceCraftId['Kounotori'].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
                Kounotori.append(parcel)
                packetCount += 1
            elif spaceCraftId['Dragon'].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
                spaceCraftId['Dragon'].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
                Dragon.append(parcel)
                packetCount += 1

        if packetCount > memorycount:
            memorycount = packetCount
            print ('<<Info>>')
            print (list(combi)[:packetCount])
            print (packetCount)
            print ('<<Info>>')
            print ("Progress", Progress)
            print ('---------------')
            print ("Cygnus", Cygnus)
            print ('---------------')
            print ("Kounotori", Kounotori)
            print ('---------------')
            print ("Dragon", Dragon)
            print ('---------------')
            print ("Progress", len(Progress), "Cygnus", len(Cygnus), "Kounotori", len(Kounotori), "Dragon", len(Dragon), "\n")

            for y in spaceCraftId.keys():
                print(y)
                print ("Payload (current, max)", spaceCraftId[y].currentPayload, spaceCraftId[y].maxPayload,
                   str(round(spaceCraftId[y].currentPayload / spaceCraftId[y].maxPayload * 100, 2)) + "%")
                print ("PayloadMass (current, max)", spaceCraftId[y].currentPayloadMass, spaceCraftId[y].maxPayloadMass, 
                   str(round(spaceCraftId[y].currentPayloadMass / spaceCraftId[y].maxPayloadMass * 100, 2)) + "%")
            endtime = time.time()
            print("Tijd: ", endtime - starttime)

if __name__ == '__main__':
    bruteforce()

