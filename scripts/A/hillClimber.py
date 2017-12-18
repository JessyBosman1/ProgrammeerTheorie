import sys
sys.path.append("..")
import supportFunctionsHillClimber as supportHC
import main
import csv

def hillclimberA(numberofruns):
	""" Applies the hillclimber algorithm to get a result for 
		question A.
	"""
	spaceCraftId = main.createObjectsSpaceCraft()
	cargoListId = main.createObjectsCargoList()
	random_runs = numberofruns
	counter = 0
	while(counter<random_runs):
		supportHC.hillClimber("random1.csv","random1Attempt_100x_1000000_20_5.csv","highScore_A.csv",cargoListId,spaceCraftId,[],False,5,10000,20)
		counter += 1

if __name__ == "__main__":
	random_runs = 200000
	hillclimberA(random_runs)