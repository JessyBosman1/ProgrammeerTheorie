import sys
sys.path.append("..")
import supportFunctionsHillClimber as supportHC
import main
import csv

if __name__ == "__main__":
	spaceCraftId = main.createObjectsSpaceCraft()
	cargoListId = main.createObjectsCargoList(2)
	random_runs = 200000
	counter = 0
	while(counter<random_runs):
		supportHC.hillClimber("randomList2.csv","random2Attempt_100x_1000000_20_5.csv","highScore_C.csv",cargoListId,spaceCraftId,5,100000,20)
