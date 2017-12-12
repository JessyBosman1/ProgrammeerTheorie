import random
import itertools
import sys
sys.path.append("..")
import main
import SolutionA
import csv


spaceCraftId = main.createObjectsSpaceCraft()
cargoListId = main.createObjectsCargoList(2)


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
	cargoListId = main.createObjectsCargoList(2)
	output = {}
	output["attempt"] = {}
	for ship in range(0,len(spaceList)):
		output["attempt"][spaceList[ship]]={parcel:0 for parcel in dividedParcels[ship]}
	SolutionA.getBestRun(output, spaceList, filename,True, False, True)

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

def hillClimber(filename, saveFile, removedParcels=5, totalIter=10000, attemptIter=20):
	"""De hill climber functie zelf, gaat met dmv random toewijzingen opzoek naar verbeteringen"""
	recordBroken = 0
	unchanged = 0
	spaceList, dividedParcels = openResults(filename)
	runs = 0
	usedParcels, unusedParcels, allParcels = getParcels(dividedParcels)
	prepareSpaceCrafts(spaceList,dividedParcels)
	highEfficiencyScore = getEfficiency(spaceList)
	while(runs <= totalIter):
		combinationRuns = 0
		runs += 1
		if runs %250 == 0:
			unchanged += 1
			print(runs*attemptIter, recordBroken)
			if unchanged == 25:
				sendToSave(dividedParcels, spaceList, "record1.csv")
				return
				
		chosenParcels = parcelPicker(usedParcels, removedParcels)
		#Combination attempt
		while (combinationRuns <= attemptIter):
			highScore = getScore(dividedParcels)

			usedParcels, unusedParcels, allParcels = getParcels(dividedParcels)
			combinationRuns += 1
			dividedAttempt, unusedAttempt = parcelRemover(chosenParcels, dividedParcels, unusedParcels)
			prepareSpaceCrafts(spaceList, dividedAttempt)
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

			if (getScore(dividedAttempt)>=highScore and highEfficiencyScore>getEfficiency(spaceList)):
				print(getScore(dividedAttempt), highScore)
				unchanged = 0
				sendToSave(dividedAttempt,spaceList, saveFile)
				highEfficiencyScore=getEfficiency(spaceList)
				recordBroken += 1
				dividedParcels = []
				for x in dividedAttempt:
					dividedParcels.append(x)
			elif(getScore(dividedAttempt)>highScore):
				unchanged = 0
				print(getScore(dividedAttempt), highScore)
				sendToSave(dividedAttempt,spaceList, saveFile)
				highEfficiencyScore=getEfficiency(spaceList)
				recordBroken += 1
				dividedParcels = []
				for x in dividedAttempt:
					dividedParcels.append(x)


if __name__ == '__main__':
	spaceCraftId = main.createObjectsSpaceCraft()
	cargoListId = main.createObjectsCargoList(2)
	random_runs = 200000
	counter = 0
	while(counter<random_runs):
		hillClimber("randomList2.csv","random2Attempt_100x_1000000_20_5.csv",5,100000,20)
