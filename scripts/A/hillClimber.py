import sys
sys.path.append("..")
import supportFunctionsHillClimber as supportHC
import main
import csv

if __name__ == "__main__":
	spaceCraftId = main.createObjectsSpaceCraft()
	cargoListId = main.createObjectsCargoList()
	random_runs = 200000
	counter = 0
	while(counter<random_runs):
		supportHC.hillClimber("random1.csv","random1Attempt_100x_1000000_20_5.csv","highScore_A.csv",cargoListId,spaceCraftId,5,10000,20)
