import csv
import os.path
import random
import itertools
import sys
sys.path.append("..")
import main
spaceCraftId = main.createObjectsSpaceCraft()
cargoListId = main.createObjectsCargoList()

for craft in spaceCraftId.keys():
    print (spaceCraftId['Cygnus'].maxPayload)

print(spaceCraftId['Cygnus'].calculateFuel())


# little check to see the total parcel weight and volume
print ('<<TOTAL LOAD>>')
totalWeight = 0
totalVolume = 0
for parcel in cargoListId.keys():
    totalWeight = totalWeight + cargoListId[parcel].weight
    totalVolume = totalVolume + cargoListId[parcel].volume
print (totalWeight)
print (totalVolume)

# <<ASSIGNMENT 1>>
# create all permutations of cargolist
combinations = itertools.permutations(cargoListId.keys(), len(cargoListId.keys()))

# use counter to prematurely break loop to prevent a large amount of loops
counter = 0
# used to remember last iteration, to skip the loop if the fitting parcels would be the same
lastIteration = []
packetCount = 1

for combi in combinations:
    # if the new list has the same packets in front as fitted in the one before, skip iteration
    # <! used for optimalisation >
    if list(combi)[:packetCount] == lastIteration[:packetCount]:
        continue
    lastIteration = list(combi)

    counter += 1
    # keep track of the number of parcels in the spaceCrafts
    packetCount = 0

    # reset parameters of spacecraft / clear loading hold of spacecraft
    spaceCraftId['Progress'].reset()
    spaceCraftId['Cygnus'].reset()
    spaceCraftId['Kounotori'].reset()
    spaceCraftId['Dragon'].reset()

    # for every parcel in combination
    for parcel in combi:
        # if there is room: add
        if spaceCraftId['Progress'].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
            spaceCraftId['Progress'].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
            packetCount += 1
        elif spaceCraftId['Cygnus'].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
            spaceCraftId['Cygnus'].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
            packetCount += 1
        elif spaceCraftId['Kounotori'].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
            spaceCraftId['Kounotori'].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
            packetCount += 1
        elif spaceCraftId['Dragon'].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
            spaceCraftId['Dragon'].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
            packetCount += 1

    if packetCount > 90:
        print ('<<Info>>')
        print (list(combi)[:packetCount])
        print (packetCount)
        #print (spaceCraftId['Progress'].currentPayloadMass)
        #print (spaceCraftId['Progress'].currentPayload)
        #print (spaceCraftId['Progress'].maxPayloadMass)
        #print (spaceCraftId['Progress'].maxPayload)
        break

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
