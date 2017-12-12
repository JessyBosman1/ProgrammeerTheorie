import random
import itertools
import os
import sys
sys.path.append("..")
import main
import preparation
import csv

def getBestRun(attempt, spacelist, filename, printResults=False, storeResults=True, addResults=False):
    """Deze functie vindt de beste run en slaat deze naderhand op in de aangewezen csv.
    Met printresults kan je de informatie terugvinden in je terminal"""
    spaceCraftId = main.createObjectsSpaceCraft()
    cargoListId = main.createObjectsCargoList(2)
    craftOrder = [order for order in attempt.keys()]
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

def logicalSolution():
    spaceCraftId = main.createObjectsSpaceCraft()
    cargoListId = main.createObjectsCargoList(2)
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
            chosen, volumeList, weightList = preparation.top50Maker(1)

            # Remove already added parcels
            for x in done:
                if x in chosen:
                    chosen.remove(x)
                    volumeList.remove(x)
                    weightList.remove(x)

            # Loops through all the parcels
            for x in range(0, len(chosen)):
                # Finds the optimal parcel
                parcel, symbol = preparation.findSpace(spaceCraftId, ship, chosen, volumeList, weightList)

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

    filename = "solutionA.csv"
    path = "../savedResults"
    fullpath = os.path.join(path, filename)

    getBestRun(attempt, spaceList, fullpath, True)

#logicalSolution()