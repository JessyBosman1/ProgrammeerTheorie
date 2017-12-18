
import sys
sys.path.append("..")
import supportFunctionsHillClimber as supportHC
import main
import csv
def HillClimberD():
	""" Uses a division of parcels over 9 shipments(Calculated with a hillclimber) to optimize the sendings."""
	
	# Prepares the variables
	spaceCraftId = main.createObjectsSpaceCraft("DE")
	cargoListName = "SwitchD"
	cargoListIdOld = main.createObjectsCargoList(3)
	startFile = "records/OptimalRandomList.csv"
	FilledInParcels = []
	usedParcels = []
	unusedParcels = supportHC.MakeTemporaryCargoList(cargoListIdOld,"records/resultsFirstHalf.csv",cargoListName,0,True)
	reDoFile = "records/Used.csv"
	# First iteration uses the original division from OptimalRandomList.csv 
	for x in range(0,8):
		supportHC.MakeTemporaryCargoList(cargoListIdOld,"records/resultsFirstHalf.csv",cargoListName,x)
		cargoListId = main.createObjectsCargoList(cargoListName)
		supportHC.generateRandomList(startFile,cargoListId,spaceCraftId)
		saveFile = "records/OptimalFirstRun"+str(x)+".csv"
		usedParcels, unusedAttempt = supportHC.hillClimber(startFile, "records/OptimalResultsD.csv", saveFile, cargoListId, spaceCraftId, [], False, 5, 100000, 20, 15, True, True)
		
		# Store the unused Parcels to use later on
		unusedParcels = unusedParcels + unusedAttempt
		FilledInParcels.append(usedParcels)
	supportHC.SaveToRetry(reDoFile,FilledInParcels)
	
	# Try to switch around to try to fit the remaining parcels in anyway
	for x in range(0,8):
		startFile = "records/OptimalFirstRun"+str(x)+".csv"
		supportHC.MakeTemporaryCargoList(cargoListIdOld,reDoFile,cargoListName,x,False,unusedParcels)
		cargoListId = main.createObjectsCargoList(cargoListName)
		supportHC.generateRandomList(startFile,cargoListId,spaceCraftId)
		unusedParcels = supportHC.hillClimber(startFile, "records/OptimalResultsD.csv", "records/OptimalFinalResulsts.csv", cargoListId, spaceCraftId, [], False, 5, 100000, 20, 15, True, True)[1]

	# Send 1 more shipment to send the last parcels
	startFile = "records/OptimalRandomList.csv"
	supportHC.SaveToRetry(reDoFile,[unusedParcels])
	supportHC.MakeTemporaryCargoList(cargoListIdOld,reDoFile,cargoListName,0,False)
	cargoListId = main.createObjectsCargoList(cargoListName)
	supportHC.generateRandomList(startFile,cargoListId,spaceCraftId)
	supportHC.hillClimber(startFile, "records/OptimalResultsD.csv", "records/OptimalFinalResulsts.csv", cargoListId, spaceCraftId, [], False, 5, 100000, 20, 15, True)

if __name__ == '__main__':
	HillClimberD()













