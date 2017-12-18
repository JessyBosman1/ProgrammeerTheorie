import sys
sys.path.append("..")
import supportFunctionsHillClimber as supportHC
import main
import csv
def HillClimberC():
	spaceCraftId = main.createObjectsSpaceCraft()
	cargoListId = main.createObjectsCargoList(2)
	random_runs = 200000
	counter = 0
	while(counter<random_runs):
		# For further explanation, check supportFunctionsHillClimber.py
		supportHC.hillClimber("records/randomList2.csv","records/random2Attempt_100x_1000000_20_5.csv","records/highScore_C.csv",cargoListId,spaceCraftId,[],False,5,100000,20)

if __name__ == "__main__":
	HillClimberC()