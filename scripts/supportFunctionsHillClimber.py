import csv
import main
import random
import itertools
import sys

spaceCraftId = main.createObjectsSpaceCraft()
cargoListId = main.createObjectsCargoList()

def openResults(filename):
	"""Haalt de attempt op uit een csv-bestand en returnt de spacelist
	 en de verdeling"""
	with open(filename, "r") as file:
		reader = csv.reader(file)
		dividedParcels = list(reader)

	spaceList = dividedParcels[0]
	dividedParcels = dividedParcels[1:]
	return spaceList, dividedParcels

def getParcels(dividedParcels):
    """Vind alle ontbekende parcels die niet in de schepen zitten en returnt
    deze samen met een lijst van alle gebruikte parcels"""
    usedParcels = [parcel for ship in dividedParcels for parcel in ship]
    unusedParcels = [parcel for parcel in cargoListId if parcel not in usedParcels]
    allParcels = [parcel for parcel in cargoListId]
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

def prepareSpaceCrafts(spaceList, dividedParcels):
	"""Maakt de schepen klaar om mee te testen"""
	for ship in range(0,len(spaceList)):
		shipName = spaceList[ship]
		spaceCraftId[shipName].reset()

		for parcel in dividedParcels[ship]:
			spaceCraftId[shipName].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)

def sendToSave(dividedParcels, spaceList, filename):
	spaceCraftId = main.createObjectsSpaceCraft()
	cargoListId = main.createObjectsCargoList()
	output = {}
	output["attempt"] = {}
	for ship in range(0,len(spaceList)):
		output["attempt"][spaceList[ship]]={parcel:0 for parcel in dividedParcels[ship]}
	getBestRun(output, spaceList, filename,True, False, True)

def getScore(dividedAttempt):
	countParcels = 0
	for ship in dividedAttempt:
		countParcels += len(ship)
	return countParcels

def getShipOrder(spaceList):
	return sorted(spaceList, key=lambda k: random.random())

def getEfficiency(spaceList):
	percentageCounter = [0,0]
	for ship in spaceList:
		percentageCounter[0] += spaceCraftId[ship].currentPayload / spaceCraftId[ship].maxPayload * 100
		percentageCounter[1] += spaceCraftId[ship].currentPayloadMass / spaceCraftId[ship].maxPayloadMass * 100
	percentageCounter[0] = percentageCounter[0]/len(spaceList)
	percentageCounter[1] = percentageCounter[1]/len(spaceList)
	return sum(percentageCounter)/2

def getBestRun(attempt, spacelist, filename, printResults=False, storeResults=True, addResults=False, cargoListNuber=1):
    """Deze functie vindt de beste run en slaat deze naderhand op in de aangewezen csv.
    Met printresults kan je de informatie terugvinden in je terminal"""
    spaceCraftId = main.createObjectsSpaceCraft()
    cargoListId = main.createObjectsCargoList(cargoListNuber)
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
        with open(filename, 'w') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(spacelist)
            for x in output:
                spamwriter.writerow(x)

    elif addResults:
        # voegt het toe aan de csv
        with open(filename, 'a') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            firstRow = []
            for y in spacelist:
                firstRow.append(y)
            firstRow.append(highAmount)
            firstRow.append(highPercentage)
            spamwriter.writerow(firstRow)
            for x in output:
                spamwriter.writerow(x)
