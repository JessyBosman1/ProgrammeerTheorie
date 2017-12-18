import csv
import main
import random
import itertools
import sys

def MakeTemporaryCargoList(oldCargolistId, filenameSendings, outputFilename,wantedShipment,unusedInCsv=False, AddExtraParcels=[]):
    """ Creates a temporary Cargolist to use to hillclimber efficiently over multiple shipments
    """
    # Opens the csv and retrieves the required data
    unusedParcels, sending = openResults(filenameSendings,unusedInCsv)
    sending = sending[wantedShipment]

    # Creates the name of the new Cargolist
    CurrentCargoList = '../../data/CargoList' + outputFilename + '.csv'

    # Creates the csv-file and saves the data of the parcels in it
    with open(CurrentCargoList, "w", newline='') as file:
        spamwriter = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['parcel_ID','weight (kg)','volume (m^3)'])
        # For each parcel the Name, Weight and Volume is taken from the main Cargolist
        for item in sending:
            stats = []
            stats.append(item)
            stats.append(oldCargolistId[item].weight)
            stats.append(oldCargolistId[item].volume)
            spamwriter.writerow(stats)
        # AddExtraParcels contains never before used parcels which need to be used later
        for extra in AddExtraParcels:
            if extra not in sending:
                stats = []
                stats.append(extra)
                stats.append(oldCargolistId[extra].weight)
                stats.append(oldCargolistId[extra].volume)
                spamwriter.writerow(stats)
    # This returns the requested unused Parcels, retrieved from the openResults function
    if unusedInCsv:
        return unusedParcels

def SaveToRetry(filename, UsedList):
    """ Saves the lists of shipments in a csv file"""
    name = [x for x in range(0,len(UsedList))]
    # This creates a new csv file to store the shipments in
    with open(filename, "w", newline='') as file:
        spamwriter = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(name)
        for item in UsedList:
            spamwriter.writerow(item)

def openResults(filename,unusedInCsv=False):
    """Retrieves an attempt and returns the division of parcels in a list of list and the ships.
    If unusedInCsv is true, then it returns the unused parcels and the divided parcels"""
    if(not unusedInCsv):
        # Opens the requested file and extracts the data
        with open(filename, "r") as file:
            reader = csv.reader(file)
            dividedParcels = list(reader)

        spaceList = dividedParcels[0]
        dividedParcels = dividedParcels[1:]
        return spaceList, dividedParcels
    else:
        # Opens the requested file and extracts the data
        with open(filename, "r") as file:
            reader = csv.reader(file)
            dividedParcels = list(reader)

        unusedParcels = dividedParcels[-1]
        dividedParcels = dividedParcels[1:-1]
        return unusedParcels, dividedParcels

def generateRandomList(filename, cargoListId, spaceCraftId, usedParcels=[]):
    """ Generates randomly filled ship, to use as starting point to fill these ships"""
    spaceList = [spaceCraftId[ship].spacecraft for ship in spaceCraftId]
    parcels = [cargoListId[parcel].cargoId for parcel in cargoListId if parcel not in usedParcels]
    output  = []
    output.append(spaceList)
    # For each ship it will append 1 random parcel to a ship
    for x in range(0,len(spaceList)):
        parcelContainer = []
        added = False
        # While not every ship doesn't have a parcel, keep trying to add a parcel
        while(not added):
            chosenParcel = random.choice(parcels)
            if chosenParcel not in parcelContainer:
                parcelContainer.append(random.choice(parcels))
                output.append(parcelContainer)
                added = True
    # Stores the random list in a csv
    with open(filename, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for x in output:
                spamwriter.writerow(x)


def getParcels(dividedParcels, cargoListId, spaceCraftId,uParcels=[]):
    """Collects and sorts all the parcels in three categories"""
    usedParcels = [parcel for ship in dividedParcels for parcel in ship if parcel not in uParcels]
    unusedParcels = [parcel for parcel in cargoListId if parcel not in usedParcels and parcel not in uParcels]
    allParcels = [parcel for parcel in cargoListId if parcel not in uParcels]
    return usedParcels, unusedParcels, allParcels

def parcelPicker(usedParcels, amount=10):
	"""Chooses n random parcels to remove from from your ships"""
	chosenParcels = []

	for x in range(0, amount):
		parcel = random.choice(usedParcels)

		if parcel not in chosenParcels:
			chosenParcels.append(parcel)

	return chosenParcels

def parcelRemover(chosenParcels, dividedParcels, unusedParcels):
	""" Removes the chosen parcels from the assigned parcels
        and add them to the unused parcel list"""
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
	""" Prepares all the ships to restart an attempt"""
	for ship in range(0,len(spaceList)):
		shipName = spaceList[ship]
		spaceCraftId[shipName].reset()

		for parcel in dividedParcels[ship]:
			spaceCraftId[shipName].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)

def sendToSave(dividedParcels, spaceList, filename, cargoListId, spaceCraftId):
	""" Prepares the input to print and save the results of the new highscore"""
    output = {}
    output["attempt"] = {}
    for ship in range(0,len(spaceList)):
        output["attempt"][spaceList[ship]]={parcel:0 for parcel in dividedParcels[ship]}
    getBestRun(output,spaceList,filename,cargoListId,spaceCraftId,True,False,True)

def getScore(dividedAttempt):
    """ Counts the amount of parcels in the shipment"""
	countParcels = 0
	for ship in dividedAttempt:
		countParcels += len(ship)
	return countParcels

def getShipOrder(spaceList):
    """ Returns a list of ships placed in a random order"""
	return sorted(spaceList, key=lambda k: random.random())

def getEfficiency(spaceList, cargoListId, spaceCraftId):
    """ Calculates the efficiency of the ship, i.e. how full the ship is"""
	percentageCounter = [0,0]
	
    # For each ship we will calculate the percentage of fullness, in volume or mass
    for ship in spaceList:
		percentageCounter[0] += spaceCraftId[ship].currentPayload / spaceCraftId[ship].maxPayload * 100
		percentageCounter[1] += spaceCraftId[ship].currentPayloadMass / spaceCraftId[ship].maxPayloadMass * 100
	# Then we take the mean of the total means
    percentageCounter[0] = percentageCounter[0]/len(spaceList)
	percentageCounter[1] = percentageCounter[1]/len(spaceList)
    # Finally we return the sum of the normalized volume and weight, divided by 2
	return sum(percentageCounter)/2

def getFinancialResult(spaceList,cargoListId,spaceCraftId):
    """ Calculate the total price of a shipment"""
    price = 0
    for ship in spaceList:
        # If a ship is not empty, then add the Base cost
        if spaceCraftId[ship].currentPayloadMass!=0:
            fuel = spaceCraftId[ship].calculateFuel()
            price += spaceCraftId[ship].calculateCost(fuel)
    return price


def getBestRun(attempt, spacelist, filename, cargoListId, spaceCraftId, printResults=False, storeResults=True, addResults=False):
    """Deze functie vindt de beste run en slaat deze naderhand op in de aangewezen csv.
    Met printresults kan je de informatie terugvinden in je terminal

    This function finds the best run in a dict of attempts and stores this run in an assigned csv.
    It is also used as the main store function of hillclimber."""
    craftOrder = [order for order in attempt.keys()]
    highPercentage = [0,0]
    highAmount = 0
    bestOrder = ""
    output = []

    # Loops through all possible permutations of ship orders
    for order in craftOrder:
        outputPreparation = []
        parcelCounter = 0
        percentageCounter = [0,0]

        # Checks every ship
        for ship in spacelist:
            outputPreparation.append([parcel for parcel in attempt[order][ship].keys()])
            spaceCraftId[ship].reset()

            # Prepares each class, so that calculates could be made
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

def hillClimber(filename, saveFile, highscoreFile, cargoListId, spaceCraftId, uParcels=[], returnUsedParcels=False, removedParcels=5, totalIter=10000, attemptIter=20, failRule=25, financialConstraint=False, returnUnusedParcels=False):
    """De hill climber functie zelf, gaat met dmv random toewijzingen opzoek naar verbeteringen"""
    recordBroken = 0
    unchanged = 0
    spaceList, dividedParcels = openResults(filename)
    runs = 0
    usedParcels, unusedParcels, allParcels = getParcels(dividedParcels, cargoListId, spaceCraftId,uParcels)
    prepareSpaceCrafts(spaceList,dividedParcels, cargoListId, spaceCraftId)
    highEfficiencyScore = getEfficiency(spaceList, cargoListId, spaceCraftId)
    if(financialConstraint):
        lowestPriceScore = getFinancialResult(spaceList,cargoListId,spaceCraftId)
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
                elif returnUnusedParcels:
                    used, unused, useless = getParcels(dividedParcels, cargoListId, spaceCraftId, uParcels)
                    return used, unused
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


            if (financialConstraint):
                if (getScore(dividedAttempt)>=highScore and highEfficiencyScore>getEfficiency(spaceList, cargoListId, spaceCraftId) and lowestPriceScore>getFinancialResult(spaceList,cargoListId,spaceCraftId)):
                    lowestPriceScore = getFinancialResult(spaceList, cargoListId, spaceCraftId)
                    print(getScore(dividedAttempt), highScore, lowestPriceScore)
                    unchanged = 0
                    sendToSave(dividedAttempt,spaceList, saveFile, cargoListId, spaceCraftId)
                    highEfficiencyScore=getEfficiency(spaceList, cargoListId, spaceCraftId)
                    recordBroken += 1
                    dividedParcels = []
                    for x in dividedAttempt:
                        dividedParcels.append(x)
                elif(getScore(dividedAttempt)>highScore):
                    unchanged = 0
                    print(getScore(dividedAttempt), highScore, lowestPriceScore)
                    sendToSave(dividedAttempt,spaceList, saveFile, cargoListId, spaceCraftId)
                    highEfficiencyScore=getEfficiency(spaceList, cargoListId, spaceCraftId)
                    lowestPriceScore = getFinancialResult(spaceList, cargoListId, spaceCraftId)
                    recordBroken += 1
                    dividedParcels = []
                    for x in dividedAttempt:
                        dividedParcels.append(x)
            else:
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
    sendToSave(dividedParcels, spaceList, highscoreFile, cargoListId, spaceCraftId)
    if returnUsedParcels:
        return getParcels(dividedParcels, cargoListId, spaceCraftId, uParcels)[0]
    elif returnUnusedParcels:
        used, unused, useless = getParcels(dividedParcels, cargoListId, spaceCraftId, uParcels)
        return used, unused
    else:
        return

