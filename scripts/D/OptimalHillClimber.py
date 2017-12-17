
import sys
sys.path.append("..")
import supportFunctionsHillClimber as supportHC
import main
import csv



if __name__ == '__main__':
	spaceCraftId = main.createObjectsSpaceCraft("Shipments")
	cargoListId = main.createObjectsCargoList(3)
	spaceCraftIdSecond = main.createObjectsSpaceCraft("Shipments2") 
	startFile = "randomShipments.csv"
	supportHC.generateRandomList(startFile,cargoListId,spaceCraftId)
	used_parcels = supportHC.hillClimber(startFile,"DividingShipmentTracker.csv","DividingShipmentResults.csv",cargoListId,spaceCraftId,[],True,12,10000,10,10)
	supportHC.generateRandomList(startFile,cargoListId,spaceCraftId,used_parcels)
	supportHC.hillClimber(startFile,"DividingShipmentTracker.csv","DividingShipmentResults.csv",cargoListId,spaceCraftIdSecond,used_parcels,False,12,10000,10,10)