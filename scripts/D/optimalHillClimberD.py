
import sys
sys.path.append("..")
import supportFunctionsHillClimber as supportHC
import main
import csv
def HillClimberD():
	spaceCraftId = main.createObjectsSpaceCraft("DE")
	cargoListName = "SwitchD"
	cargoListIdOld = main.createObjectsCargoList(3)
	startFile = "OptimalRandomList.csv"
	FilledInParcels = []
	usedParcels = []
	unusedParcels = supportHC.MakeTemporaryCargoList(cargoListIdOld,"resultsFirstHalf.csv",cargoListName,0,True)
	reDoFile = "Used.csv"
	for x in range(0,8):
		supportHC.MakeTemporaryCargoList(cargoListIdOld,"resultsFirstHalf.csv",cargoListName,x)
		cargoListId = main.createObjectsCargoList(cargoListName)
		supportHC.generateRandomList(startFile,cargoListId,spaceCraftId)
		saveFile = "OptimalFirstRun"+str(x)+".csv"
		usedParcels, unusedAttempt = supportHC.hillClimber(startFile, "OptimalResultsD.csv", saveFile, cargoListId, spaceCraftId, [], False, 5, 100000, 20, 15, True, True)
		unusedParcels = unusedParcels + unusedAttempt
		FilledInParcels.append(usedParcels)
	supportHC.SaveToRetry(reDoFile,FilledInParcels)
	# Fitting in the remaining Parcels
	for x in range(0,8):
		startFile = "OptimalFirstRun"+str(x)+".csv"
		supportHC.MakeTemporaryCargoList(cargoListIdOld,reDoFile,cargoListName,x,False,unusedParcels)
		cargoListId = main.createObjectsCargoList(cargoListName)
		supportHC.generateRandomList(startFile,cargoListId,spaceCraftId)
		unusedParcels = supportHC.hillClimber(startFile, "OptimalResultsD.csv", "OptimalFinalResulsts.csv", cargoListId, spaceCraftId, [], False, 5, 100000, 20, 15, True, True)[1]

	startFile = "OptimalRandomList.csv"
	supportHC.SaveToRetry(reDoFile,[unusedParcels])
	supportHC.MakeTemporaryCargoList(cargoListIdOld,reDoFile,cargoListName,0,False)
	cargoListId = main.createObjectsCargoList(cargoListName)
	supportHC.generateRandomList(startFile,cargoListId,spaceCraftId)
	supportHC.hillClimber(startFile, "OptimalResultsD.csv", "OptimalFinalResulsts.csv", cargoListId, spaceCraftId, [], False, 5, 100000, 20, 15, True)

if __name__ == '__main__':
	HillClimberD()













