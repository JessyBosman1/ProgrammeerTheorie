import csv
import os.path
import random
import itertools
import main
from random import shuffle
spaceCraftId = main.createObjectsSpaceCraft()
cargoListId = main.createObjectsCargoList()

"""for craft in spaceCraftId.keys():
    print (spaceCraftId['Cygnus'].maxPayload)

print spaceCraftId['Cygnus'].calculateFuel()


# little check to see the total parcel weight and volume
print ('<<TOTAL LOAD>>')
totalWeight = 0
totalVolume = 0
for parcel in cargoListId.keys():
    totalWeight = totalWeight + cargoListId[parcel].weight
    totalVolume = totalVolume + cargoListId[parcel].volume
print (totalWeight)
print (totalVolume)"""

# <<ASSIGNMENT 1>>
# create all permutations of cargolist
#combinations = itertools.permutations(cargoListId.keys(), len(cargoListId.keys()))

# use counter to prematurely break loop to prevent a large amount of loops
counter = 0
# used to remember last iteration, to skip the loop if the fitting parcels would be the same
memory = []
packetCount = 0
memoryCount = 0

spaceList = ['Progress', 'Cygnus', 'Kounotori', 'Dragon']
shuffleGen = itertools.permutations(spaceList, len(spaceList))
shuffleList = [x for x in shuffleGen]

#randomList = random.sample(range(1,101), 100)
#print len(randomList)
randomList = [x for x in range(1,101)]
randomList.remove(83)
randomList.remove(58)
randomList.remove(34)

for loop in range(1000000):
    if loop%10000 == 0:
        print(loop)
    # if the new list has the same packets in front as fitted in the one before, skip iteration
    # <! used for optimalisation >
    #if list(combi)[:packetCount] == lastIteration[:packetCount]:
    #    continue
    #lastIteration = list(combi)
    # Check if the randomList was generated before
    random.shuffle(randomList)
    #print randomList
    #print len(randomList)

    #if randomList in memory:
    #    print ('double')
    #    continue
    #else:
    #    memory.append(randomList)

    # keep track of the number of parcels in the spaceCrafts
    packetCount = 0

    # reset parameters of spacecraft / clear loading hold of spacecraft

    parcelList = set()
    # for every parcel in the randomlist
    for spacer in shuffleList:
        spaceCraftId['Progress'].reset()
        spaceCraftId['Cygnus'].reset()
        spaceCraftId['Kounotori'].reset()
        spaceCraftId['Dragon'].reset()
        packetCount = 0

        space0 = []
        space1 = []
        space2 = []
        space3 = []

        for i in randomList:
            parcel = 'CL1#' + str(i)
            parcelList.add(parcel)

            # if there is room: add
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

        if packetCount > 77:
            print (len(parcelList))
            print ('<<Info>>')
            print (spacer[0], space0)
            print ("Payload (current, max)", spaceCraftId[spacer[0]].currentPayload, spaceCraftId[spacer[0]].maxPayload)
            print ("PayloadMass (current, max)", spaceCraftId[spacer[0]].currentPayloadMass, spaceCraftId[spacer[0]].maxPayloadMass)
            print ('---------------')
            print (spacer[1], space1)
            print ("Payload (current, max)", spaceCraftId[spacer[1]].currentPayload, spaceCraftId[spacer[1]].maxPayload)
            print ("PayloadMass (current, max)", spaceCraftId[spacer[1]].currentPayloadMass, spaceCraftId[spacer[1]].maxPayloadMass)
            print ('---------------')
            print (spacer[2], space2)
            print ("Payload (current, max)", spaceCraftId[spacer[2]].currentPayload, spaceCraftId[spacer[2]].maxPayload)
            print ("PayloadMass (current, max)", spaceCraftId[spacer[2]].currentPayloadMass, spaceCraftId[spacer[2]].maxPayloadMass)
            print ('---------------')
            print (spacer[3], space3)
            print ("Payload (current, max)", spaceCraftId[spacer[3]].currentPayload, spaceCraftId[spacer[3]].maxPayload)
            print ("PayloadMass (current, max)", spaceCraftId[spacer[3]].currentPayloadMass, spaceCraftId[spacer[3]].maxPayloadMass)
            print ('---------------')
            print (spacer[0], len(space0), spacer[1], len(space1), spacer[2], len(space2), spacer[3], len(space3), "\n")

            # set packet count and use correction track number of packets to remove from packetcount
            packeCount = 78
            correction = 0
            # find Id's of names from spacers
            for i in range(4):
                if spacer[i] == "Cygnus":
                    CygnusId = i
                    if CygnusId == 0:
                        correction += len(space0)
                        spaceCraftId['Cygnus'].reset()
                        space0 = []
                    elif CygnusId == 1:
                        correction += len(space1)
                        spaceCraftId['Cygnus'].reset()
                        space1 = []
                    elif CygnusId == 2:
                        correction += len(space2)
                        spaceCraftId['Cygnus'].reset()
                        space2 = []
                    elif CygnusId == 3:
                        correction += len(space3)
                        spaceCraftId['Cygnus'].reset()
                        space3 = []

            for i in range(4):
                if spacer[i] == "Dragon":
                    DragonId = i
                    if DragonId == 0:
                        correction += len(space0)
                        spaceCraftId['Dragon'].reset()
                        space0 = []
                    elif DragonId == 1:
                        correction += len(space1)
                        spaceCraftId['Dragon'].reset()
                        space1 = []
                    elif DragonId == 2:
                        correction += len(space2)
                        spaceCraftId['Dragon'].reset()
                        space2 = []
                    elif DragonId == 3:
                        correction += len(space3)
                        spaceCraftId['Dragon'].reset()
                        space3 = []

            # create new random shuffle
            spaceList = ['Cygnus', 'Dragon']
            shuffleGen = itertools.permutations(spaceList, len(spaceList))
            shuffleList = [x for x in shuffleGen]

            # remove used parcels
            for parcel in space0:
                parcelList.remove(parcel)
            for parcel in space1:
                parcelList.remove(parcel)
            for parcel in space2:
                parcelList.remove(parcel)
            for parcel in space3:
                parcelList.remove(parcel)
            parcelList = list(parcelList)

            for loop in range(500000):
                if loop%10000 == 0:
                    print(loop)

                random.shuffle(parcelList)

                packetCount = 78 - correction

                # reset parameters of spacecraft / clear loading hold of spacecraft
                for spacer in shuffleList:
                    spaceCraftId['Cygnus'].reset()
                    spaceCraftId['Dragon'].reset()
                    packetCount = 78 - correction


                    space0 = []
                    space1 = []

                    # for every parcel in the randomlist
                    for i in parcelList:
                        parcel = str(i)
                        # if there is room: add
                        if spaceCraftId[spacer[0]].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
                            spaceCraftId[spacer[0]].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
                            space0.append(parcel)
                            packetCount += 1
                        elif spaceCraftId[spacer[1]].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
                            spaceCraftId[spacer[1]].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
                            space1.append(parcel)
                            packetCount += 1

                    if packetCount > 79:
                        #print len(parcelList)
                        print (packetCount)
                        print ('<<Details>>')
                        print (spacer[0], space0)
                        print ("Payload (current, max)", spaceCraftId[spacer[0]].currentPayload, spaceCraftId[spacer[0]].maxPayload)
                        print ("PayloadMass (current, max)", spaceCraftId[spacer[0]].currentPayloadMass, spaceCraftId[spacer[0]].maxPayloadMass)
                        print ('---------------')
                        print (spacer[1], space1)
                        print ("Payload (current, max)", spaceCraftId[spacer[1]].currentPayload, spaceCraftId[spacer[1]].maxPayload)
                        print ("PayloadMass (current, max)", spaceCraftId[spacer[1]].currentPayloadMass, spaceCraftId[spacer[1]].maxPayloadMass)
                        print ('---------------')
                        print (spacer[0], len(space0), spacer[1], len(space1), "\n")



    if packetCount > memoryCount:
        memoryCount = packetCount
        print(memoryCount)

    ''' # Enable to make the loop stop prematurely'''
    #if counter == 100000:
    #    break

"""
Cygnus = 0
CygnusVol = 0
Progress = 0
ProgressVol = 0
Kounotori = 0
KounotoriVol = 0
Dragon = 0
DragonVol = 0
CygLoad = []

#randomList = random.sample(range(1,101), 100)
for i in randomList:
    parcel = 'CL1#' + str(i)
    print parcel
    print (cargoListId[parcel].weight, cargoListId[parcel].volume, cargoListId[parcel].cargoId)
    # Temporar
    tempMass = ((float(spaceCraftId['Cygnus'].fuelToWeight) * (Cygnus + float(spaceCraftId['Cygnus'].mass)))) / (1 - float(spaceCraftId['Cygnus'].fuelToWeight) )
    # Put the maximum weigth of the spacecraft Cygnus in a variable
    maxMassCygnus = (float(spaceCraftId['Cygnus'].payloadMass) + float(spaceCraftId['Cygnus'].mass))
    print tempMass, maxMassCygnus
    # Check if the payload or volume are smaller than the
    # payload and volume when the parcel is added
    if maxMassCygnus > (tempMass + float(cargoListId[parcel].weight)) and float(spaceCraftId['Cygnus'].payload) > (CygnusVol + float(cargoListId[parcel].volume)):
        # Add the parcel weigth to the curent weigth
        Cygnus += float(cargoListId[parcel].weight)
        # Add the colume to the current weigth
        CygnusVol += float(cargoListId[parcel].volume)
        # Add the parcel ID to the list with added parcels
        CygLoad.append(cargoListId[parcel].cargoId)

    # hier moet voor elke andere spacecraft
print CygLoad
"""
