import main
import random
import itertools

def prepareObjects():
    spaceCraftId = main.createObjectsSpaceCraft()
    cargoListId = main.createObjectsCargoList()
    nameList = [ship for ship in spaceCraftId]
    return spaceCraftId, cargoListId, nameList

def parcelNormalizer(type):
    # Retrieve objects from the main.py
    cargoListId = main.createObjectsCargoList()

    # Creating the necessary lists obtained from the object
    nameList = [parcel for parcel in cargoListId]
    weightList = [cargoListId[parcel].weight for parcel in cargoListId]
    volumeList = [cargoListId[parcel].volume for parcel in cargoListId]

    # Calculating the sum of the 2 lists
    sumWL = sum(weightList)
    sumVL = sum(volumeList)

    # vectorize values of weight and volume
    weightList = [x / sumWL for x in weightList]
    volumeList = [x / sumVL for x in volumeList]
    vectorizedParcels = {}
    input = volumeList
    if type == 2:
        input = volumeList
    elif type == 3:
        input = weightList

    # Creating a dict containing vectorized values. Key: parcelId Value: vector
    for i in range(0, len(input)):
        if type != 1:
            vector = (input[i])
        else:
            vector = ((weightList[i]) + (volumeList[i])) / 2
        vectorizedParcels[nameList[i]] = vector

    # Vectorized descending ranking of parcels, based on a combined variable between Weight and Volume
    ranking = sorted(vectorizedParcels, key=vectorizedParcels.get, reverse=False)
    return ranking


# Checks if which is more available: volume or weight if these are the same it chooses the main chosen ranking
def findSpace(spaceCrafts, ship, chosen, weightList, volumeList):
    volumeLeft = spaceCrafts[ship].currentPayload / spaceCrafts[ship].maxPayload * 100.0
    weightLeft = spaceCrafts[ship].currentPayloadMass / spaceCrafts[ship].maxPayloadMass * 100.0

    if volumeLeft<weightLeft:
        return volumeList[0], "v"
    elif volumeLeft>weightLeft:
        return weightList[0], "w"

    else:
        return chosen[0], "p"


# Makes sure that all the lists contain the samen values as the top50
def shortlistMaker(top50, toShorten):
    result=[]
    for x in toShorten:
        if x in top50:
            result.append(x)
    return result


# 1: vector, 2: volume 3: weight
def top50Maker(preference):
    if preference==1:
        top50=parcelNormalizer(1)
        parcelRankVol = shortlistMaker(top50, parcelNormalizer(2))
        parcelRankWeight = shortlistMaker(top50, parcelNormalizer(3))    
        return top50, parcelRankVol, parcelRankWeight
    
    elif preference==2:
        top50=parcelNormalizer(2)
        parcelRankVol = shortlistMaker(top50, parcelNormalizer(2))
        parcelRankWeight = shortlistMaker(top50, parcelNormalizer(3))
        return top50, parcelRankVol, parcelRankWeight
    
    else:
        top50=parcelNormalizer(3)
        parcelRankVol = shortlistMaker(top50, parcelNormalizer(2))
        parcelRankWeight = shortlistMaker(top50, parcelNormalizer(3))
        return top50, parcelRankVol, parcelRankWeight