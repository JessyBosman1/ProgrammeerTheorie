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
    spaceCraftId = main.createObjectsSpaceCraft("DE")
    cargoListId = main.createObjectsCargoList(3)
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
