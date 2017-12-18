import sys
sys.path.append("..")
import main
import csvReaderToScore

def calculatecheapest():
	# Run the calculation score function from excersice b
	price, parcellist, dollars = csvReaderToScore.calculatescore("records/highScore_C.csv", 1, 2)
	priceNR, parcellistNR, dollarsNR = csvReaderToScore.calculatescore("records/highScore_C.csv", 2, 2)
	return price, parcellist, dollars, priceNR, parcellistNR, dollarsNR

if __name__ == '__main__':
	price, parcellist, dollars, priceNR, parcellistNR, dollarsNR = calculatecheapest()
	csvReaderToScore.printResult(price, parcellist, dollars, priceNR, parcellistNR, dollarsNR)