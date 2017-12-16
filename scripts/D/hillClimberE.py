
import sys
sys.path.append("..")
import supportFunctionsHillClimber as supportHC
import main
import csv



if __name__ == '__main__':
	spaceCraftId = main.createObjectsSpaceCraft("DE")
	cargoListId = main.createObjectsCargoList(3)

	max_runs = 5
	startFile = "randomList4.csv"
	runs = 0
	parcelAmount = len([parcel for parcel in cargoListId])
	usedParcels=supportHC.getParcels(supportHC.openResults("Shipment.csv")[1], cargoListId, spaceCraftId)[0]
	while(runs< max_runs):
		counter = 1
		while(counter<2):
			supportHC.generateRandomList(startFile,cargoListId,spaceCraftId, usedParcels)

			if len(usedParcels)==0:
				counter+=1
			new_parcels = supportHC.hillClimber(startFile,"allResultsD.csv", "SecondSending.csv", cargoListId, spaceCraftId, usedParcels, True, 5,100000,20, 15)
			usedParcels = new_parcels + usedParcels
			if len(usedParcels) != parcelAmount:
				print("It's not empty: ",len(usedParcels))
				print(usedParcels)
			else:
				counter += 1
		runs +=1