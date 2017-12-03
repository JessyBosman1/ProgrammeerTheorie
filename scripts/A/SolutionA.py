import random
import itertools
import sys
sys.path.append("..")
import main
import csv

def getBestRun(attempt, spacelist, filename, printResults=False, storeResults=True, addResults=False):
    """Deze functie vindt de beste run en slaat deze naderhand op in de aangewezen csv.
    Met printresults kan je de informatie terugvinden in je terminal"""
    spaceCraftId = main.createObjectsSpaceCraft()
    cargoListId = main.createObjectsCargoList()
    craftOrder = [ order for order in attempt.keys()]
    highPercentage = [0,0]
    highAmount = 0
    bestOrder = ""
    output = []

    # bekijkt alle volgordes
    for order in craftOrder:
        outputPreparation = []
        parcelCounter = 0
        percentageCounter = [0,0]

        # bekijkt alle schepen
        for ship in spacelist:
            outputPreparation.append([parcel for parcel in attempt[order][ship].keys()])
            spaceCraftId[ship].reset()

            #Bereidt de class voor
            for parcel in attempt[order][ship]:
                spaceCraftId[ship].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
                parcelCounter += 1
            
            # Berekent het algemene percentage
            percentageCounter[0] += spaceCraftId[ship].currentPayload / spaceCraftId[ship].maxPayload * 100
            percentageCounter[1] += spaceCraftId[ship].currentPayloadMass / spaceCraftId[ship].maxPayloadMass * 100
        
        # Berekent het gemiddelde percentage
        percentageCounter[0] = percentageCounter[0]/len(spacelist)
        percentageCounter[1] = percentageCounter[1]/len(spacelist)
        
        # update highscores
        if sum(percentageCounter) / 2 > sum(highPercentage) / 2 and parcelCounter >= highAmount:
            highPercentage = percentageCounter
            highAmount = parcelCounter
            output = outputPreparation
            bestOrder = order
    
    #als printresultaten gewenst zijn, print de functie het gedetailleerd uit
    if printResults:
        print (bestOrder, highPercentage,highAmount)
        for x in range(0, len(spacelist)):
            print (spacelist[x], len(output[x]), output[x])
            print( "------------------------")



    if storeResults:
        # Slaat het op in de aangewezen csv        
        with open(filename, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(spacelist)
            for x in output:
                spamwriter.writerow(x)

    elif addResults:
        # voegt het toe aan de csv
        with open(filename, 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            firstRow = []
            for y in spacelist:
                firstRow.append(y)
            firstRow.append(highAmount)
            firstRow.append(highPercentage)
            spamwriter.writerow(firstRow)
            for x in output:
                spamwriter.writerow(x)

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
    weightList = [x/sumWL for x in weightList]
    volumeList = [x/sumVL for x in volumeList]
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
            vector = ((weightList[i]) + (volumeList[i]))/2
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

def logicalSolution():
    spaceCraftId = main.createObjectsSpaceCraft()
    cargoListId = main.createObjectsCargoList()
    nameList = [ship for ship in spaceCraftId]

    # Shuffles the ships
    spaceList = ['Progress', 'Cygnus', 'Kounotori', 'Dragon']
    shuffleGen = itertools.permutations(spaceList, len(spaceList))
    shuffleList = [x for x in shuffleGen]


    maxScore = 79
    attempt = {}
    # Loop through all the permutations
    for spacelist in shuffleList:
        total = 0
        done = []
        attempt[spacelist] = {}

        # Loop through each ship
        for ship in spacelist:
            spaceCraftId[ship].reset()
            cargo = {}
            # Change this number to choose the prefered sorting mechanism
            chosen, volumeList, weightList = top50Maker(1)

            # Remove already added parcels
            for x in done:
                if x in chosen:
                    chosen.remove(x)
                    volumeList.remove(x)
                    weightList.remove(x)

            # Loops through all the parcels
            for x in range(0, len(chosen)):
                # Finds the optimal parcel
                parcel, symbol = findSpace(spaceCraftId, ship, chosen, volumeList, weightList)

                # Checks if the parcel fits
                if spaceCraftId[ship].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
                    spaceCraftId[ship].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
                    cargo[parcel] = symbol
                    done.append(parcel)

                # Remove this parcel, added or not, from the list
                chosen.remove(parcel)
                volumeList.remove(parcel)
                weightList.remove(parcel)

            # Collects the attempts
            attempt[spacelist][ship] = cargo
            total += len(cargo)

        # Checks for highscores
        if total >= maxScore:
            maxScore = total
            for y in spacelist:
                print (y, attempt[spacelist][y])
                print ("Payload (current, max)", spaceCraftId[y].currentPayload, spaceCraftId[y].maxPayload,
                       str(round(spaceCraftId[y].currentPayload / spaceCraftId[y].maxPayload * 100, 2)) + "%")
                print ("PayloadMass (current, max)", spaceCraftId[y].currentPayloadMass, spaceCraftId[y].maxPayloadMass, 
                       str(round(spaceCraftId[y].currentPayloadMass / spaceCraftId[y].maxPayloadMass * 100, 2)) + "%")
                print (len(attempt[spacelist][y]))
                print ('---------------')

            print (total)
            print ('---------------')

    print (maxScore)
    getBestRun(attempt, spaceList,"attempt1.csv", True)
