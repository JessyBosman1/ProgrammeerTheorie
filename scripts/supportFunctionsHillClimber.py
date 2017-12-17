import csv
import main
import random
import itertools
import sys


def openResults(filename):
	"""Haalt de attempt op uit een csv-bestand en returnt de spacelist
	 en de verdeling"""
	with open(filename, "r") as file:
		reader = csv.reader(file)
		dividedParcels = list(reader)

	spaceList = dividedParcels[0]
	dividedParcels = dividedParcels[1:]
	return spaceList, dividedParcels



def generateRandomList(filename, cargoListId, spaceCraftId, usedParcels=[]):
    """Genereert een randomship met inhoud op basis van de usedparcels"""
    spaceList = [spaceCraftId[ship].spacecraft for ship in spaceCraftId]
    parcels = [cargoListId[parcel].cargoId for parcel in cargoListId if parcel not in usedParcels]
    output  = []
    output.append(spaceList)
    for x in range(0,len(spaceList)):
        parcelContainer = []
        added = False
        while(not added):
            chosenParcel = random.choice(parcels)
            if chosenParcel not in parcelContainer:
                parcelContainer.append(random.choice(parcels))
                output.append(parcelContainer)
                added = True
    with open(filename, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for x in output:
                spamwriter.writerow(x)


def getParcels(dividedParcels, cargoListId, spaceCraftId,uParcels=[]):
    """Vind alle ontbekende parcels die niet in de schepen zitten en returnt
    deze samen met een lijst van alle gebruikte parcels"""
    usedParcels = [parcel for ship in dividedParcels for parcel in ship if parcel not in uParcels]
    unusedParcels = [parcel for parcel in cargoListId if parcel not in usedParcels and parcel not in uParcels]
    allParcels = [parcel for parcel in cargoListId if parcel not in uParcels]
    return usedParcels, unusedParcels, allParcels

def parcelPicker(usedParcels, amount=10):
	"""Kiest een bepaald aantal random pakketten"""
	chosenParcels = []

	for x in range(0, amount):
		parcel = random.choice(usedParcels)

		if parcel not in chosenParcels:
			chosenParcels.append(parcel)

	return chosenParcels

def parcelRemover(chosenParcels, dividedParcels, unusedParcels):
	"""Haalt parcels uit schepen om opnieuw toe te wijzen"""
	dividedOutput = []
	for ship in dividedParcels:
		newShip = []
		for parcel in ship:
			if parcel not in chosenParcels:
				newShip.append(parcel)
			else:
				unusedParcels.append(parcel)
		dividedOutput.append(newShip)
	return dividedOutput, unusedParcels

def prepareSpaceCrafts(spaceList, dividedParcels, cargoListId, spaceCraftId):
	"""Maakt de schepen klaar om mee te testen"""
	for ship in range(0,len(spaceList)):
		shipName = spaceList[ship]
		spaceCraftId[shipName].reset()

		for parcel in dividedParcels[ship]:
			spaceCraftId[shipName].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)

def sendToSave(dividedParcels, spaceList, filename, cargoListId, spaceCraftId):
	
    output = {}
    output["attempt"] = {}
    for ship in range(0,len(spaceList)):
        output["attempt"][spaceList[ship]]={parcel:0 for parcel in dividedParcels[ship]}
    getBestRun(output,spaceList,filename,cargoListId,spaceCraftId,True,False,True)

def getScore(dividedAttempt):
	countParcels = 0
	for ship in dividedAttempt:
		countParcels += len(ship)
	return countParcels

def getShipOrder(spaceList):
	return sorted(spaceList, key=lambda k: random.random())

def getEfficiency(spaceList, cargoListId, spaceCraftId):
	percentageCounter = [0,0]
	for ship in spaceList:
		percentageCounter[0] += spaceCraftId[ship].currentPayload / spaceCraftId[ship].maxPayload * 100
		percentageCounter[1] += spaceCraftId[ship].currentPayloadMass / spaceCraftId[ship].maxPayloadMass * 100
	percentageCounter[0] = percentageCounter[0]/len(spaceList)
	percentageCounter[1] = percentageCounter[1]/len(spaceList)
	return sum(percentageCounter)/2

def getBestRun(attempt, spacelist, filename, cargoListId, spaceCraftId, printResults=False, storeResults=True, addResults=False):
    """Deze functie vindt de beste run en slaat deze naderhand op in de aangewezen csv.
    Met printresults kan je de informatie terugvinden in je terminal"""
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

def hillClimber(filename, saveFile, highscoreFile, cargoListId, spaceCraftId, uParcels=[], returnUsedParcels=False, removedParcels=5, totalIter=10000, attemptIter=20, failRule=25):
    """De hill climber functie zelf, gaat met dmv random toewijzingen opzoek naar verbeteringen"""
    recordBroken = 0
    unchanged = 0
    spaceList, dividedParcels = openResults(filename)
    runs = 0
    usedParcels, unusedParcels, allParcels = getParcels(dividedParcels, cargoListId, spaceCraftId,uParcels)
    prepareSpaceCrafts(spaceList,dividedParcels, cargoListId, spaceCraftId)
    highEfficiencyScore = getEfficiency(spaceList, cargoListId, spaceCraftId)
    while(runs <= totalIter):
        combinationRuns = 0
        runs += 1
        if runs %250 == 0:
            unchanged += 1
            print(runs*attemptIter, recordBroken)
            if unchanged == failRule:
                sendToSave(dividedParcels, spaceList, highscoreFile, cargoListId, spaceCraftId)
                if returnUsedParcels:
                    return getParcels(dividedParcels, cargoListId, spaceCraftId, uParcels)[0]
                else:
                    return

        chosenParcels = parcelPicker(usedParcels, removedParcels)
        #Combination attempt
        while (combinationRuns <= attemptIter):
            highScore = getScore(dividedParcels)

            usedParcels, unusedParcels, allParcels = getParcels(dividedParcels, cargoListId, spaceCraftId, uParcels)
            combinationRuns += 1
            dividedAttempt, unusedAttempt = parcelRemover(chosenParcels, dividedParcels, unusedParcels)
            prepareSpaceCrafts(spaceList, dividedAttempt, cargoListId, spaceCraftId)
            #placing attempt
            while (len(unusedAttempt) != 0):
                parcel = random.choice(unusedAttempt)
                toPlace = True
                #vind het juiste schip
                for ship in getShipOrder(spaceList):
                    if spaceCraftId[ship].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False and toPlace:
                        spaceCraftId[ship].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
                        dividedAttempt[spaceList.index(ship)].append(parcel)
                        toPlace = False


                unusedAttempt.remove(parcel)

            if (getScore(dividedAttempt)>=highScore and highEfficiencyScore>getEfficiency(spaceList, cargoListId, spaceCraftId)):
                print(getScore(dividedAttempt), highScore)
                unchanged = 0
                sendToSave(dividedAttempt,spaceList, saveFile, cargoListId, spaceCraftId)
                highEfficiencyScore=getEfficiency(spaceList, cargoListId, spaceCraftId)
                recordBroken += 1
                dividedParcels = []
                for x in dividedAttempt:
                    dividedParcels.append(x)
            elif(getScore(dividedAttempt)>highScore):
                unchanged = 0
                print(getScore(dividedAttempt), highScore)
                sendToSave(dividedAttempt,spaceList, saveFile, cargoListId, spaceCraftId)
                highEfficiencyScore=getEfficiency(spaceList, cargoListId, spaceCraftId)
                recordBroken += 1
                dividedParcels = []
                for x in dividedAttempt:
                    dividedParcels.append(x)

