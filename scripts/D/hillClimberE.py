
import sys
sys.path.append("..")
import supportFunctionsHillClimber as supportHC
import main
import csv

if __name__ == '__main__':
	spaceCraftId = main.createObjectsSpaceCraft("DE")
	cargoListId = main.createObjectsCargoList(3)
	max_runs = 5
	runs = 0
	while(runs< max_runs):
		counter = 0
		remainingParcels=[]

		while(counter<2):
			if len(remainingParcels)==0:
				counter+=1
			remainingParcels = supportHC.hillClimber("randomList4.csv","allResultsD.csv", "BestRuns.csv", cargoListId, spaceCraftId, remainingParcels, True, 5,100000,20, 15)
			if(remainingParcels != None):
				print("It's not empty: ",len(remainingParcels))
				print(remainingParcels)
			else:
				counter += 1

		with open("BestRuns.csv", 'a', newline='') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			spamwriter.writerow(["end attempt"])
			csvfile.close()
		runs +=1