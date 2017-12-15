import random
import itertools
import sys
sys.path.append("..")
import supportFunctionsHillClimber as supportHC
import main
import csv

spaceCraftId = main.createObjectsSpaceCraft()
cargoListId = main.createObjectsCargoList()

def hillClimber(filename, saveFile, removedParcels=5, totalIter=10000, attemptIter=20):
	"""De hill climber functie zelf, gaat met dmv random toewijzingen opzoek naar verbeteringen"""
	recordBroken = 0
	unchanged = 0
	spaceList, dividedParcels = supportHC.openResults(filename)
	runs = 0
	usedParcels, unusedParcels, allParcels = supportHC.getParcels(dividedParcels)
	supportHC.prepareSpaceCrafts(spaceList,dividedParcels)
	highEfficiencyScore = supportHC.getEfficiency(spaceList)
	while(runs <= totalIter):
		combinationRuns = 0
		runs += 1
		if runs %250 == 0:
			unchanged += 1
			print(runs*attemptIter, recordBroken)
			if unchanged == 25:
				supportHC.sendToSave(dividedParcels, spaceList, "record.csv")
				return

		chosenParcels = supportHC.parcelPicker(usedParcels, removedParcels)
		#Combination attempt
		while (combinationRuns <= attemptIter):
			highScore = supportHC.getScore(dividedParcels)

			usedParcels, unusedParcels, allParcels = supportHC.getParcels(dividedParcels)
			combinationRuns += 1
			dividedAttempt, unusedAttempt = supportHC.parcelRemover(chosenParcels, dividedParcels, unusedParcels)
			supportHC.prepareSpaceCrafts(spaceList, dividedAttempt)
			#placing attempt
			while (len(unusedAttempt) != 0):
				parcel = random.choice(unusedAttempt)
				toPlace = True
				#vind het juiste schip
				for ship in supportHC.getShipOrder(spaceList):
					if spaceCraftId[ship].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False and toPlace:
						spaceCraftId[ship].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
						dividedAttempt[spaceList.index(ship)].append(parcel)
						toPlace = False


				unusedAttempt.remove(parcel)

			if (supportHC.getScore(dividedAttempt)>=highScore and highEfficiencyScore>supportHC.getEfficiency(spaceList)):
				print(supportHC.getScore(dividedAttempt), highScore)
				unchanged = 0
				supportHC.sendToSave(dividedAttempt,spaceList, saveFile)
				highEfficiencyScore=supportHC.getEfficiency(spaceList)
				recordBroken += 1
				dividedParcels = []
				for x in dividedAttempt:
					dividedParcels.append(x)
			elif(supportHC.getScore(dividedAttempt)>highScore):
				unchanged = 0
				print(supportHC.getScore(dividedAttempt), highScore)
				supportHC.sendToSave(dividedAttempt,spaceList, saveFile)
				highEfficiencyScore=supportHC.getEfficiency(spaceList)
				recordBroken += 1
				dividedParcels = []
				for x in dividedAttempt:
					dividedParcels.append(x)

if __name__ == "__main__":
	random_runs = 200000
	counter = 0
	while(counter<random_runs):
		hillClimber("random1.csv","random1Attempt_100x_1000000_20_5.csv",5,100000,20)
