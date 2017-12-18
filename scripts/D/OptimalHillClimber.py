
import sys
sys.path.append("..")
import supportFunctionsHillClimber as supportHC
import main
import csv



if __name__ == '__main__':
	cargoListId = main.createObjectsCargoList(3)
	spaceCraftId = main.createObjectsSpaceCraft("Shipments")
	spaceCraftIdSecond = main.createObjectsSpaceCraft("Shipments2") 
	startFile = "resultsFirstHalf.csv"
	usedParcels=supportHC.getParcels(supportHC.openResults(startFile)[1], cargoListId, spaceCraftId)[0]
	supportHC.hillClimber("randomShipments.csv","DividingShipmentTracker.csv","DividingShipmentResults.csv",cargoListId,spaceCraftIdSecond,usedParcels,False,12,10000,10,10)
