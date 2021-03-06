
import sys
sys.path.append("..")
import supportFunctionsHillClimber as supportHC
import main
import csv
def HillClimberE():
	""" First attempt to calculate D with a HillClimber it stacks the usedParcels
	in a list and uses it to exclude those parcels"""
	spaceCraftId = main.createObjectsSpaceCraft("DE")
	cargoListId = main.createObjectsCargoList(3)

	max_runs = 5
	startFile = "records/randomList4.csv"
	runs = 0
	parcelAmount = len([parcel for parcel in cargoListId])
	usedParcels=supportHC.getParcels(supportHC.openResults("records/Shipment.csv")[1], cargoListId, spaceCraftId)[0]
	while(runs< max_runs):
		counter = 1
		while(counter<2):
			# It builds a random starting point
			supportHC.generateRandomList(startFile,cargoListId,spaceCraftId, usedParcels)

			if len(usedParcels)==0:
				counter+=1

			# Activating the hillCLimber
			new_parcels = supportHC.hillClimber(startFile,"records/allResultsD.csv", "records/SecondSending.csv", cargoListId, spaceCraftId, usedParcels, True, 5,100000,20, 15)
			usedParcels = new_parcels + usedParcels
			if len(usedParcels) != parcelAmount:
				print("It's not empty: ",len(usedParcels))
				print(usedParcels)
			else:
				counter += 1
		runs +=1

if __name__ == '__main__':
	HillClimberE()