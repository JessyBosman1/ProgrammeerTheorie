import sys
sys.path.append("..")
sys.path.append("../A")
import main
import csvReaderToScore

def calculatecheapest():
	# Run the calculation score function from excersice b
	price, parcellist, dollars = csvReaderToScore.calculatescore("../A/records/record.csv", 1, 1)
	priceNR, parcellistNR, dollarsNR = csvReaderToScore.calculatescore("../A/records/record.csv", 2, 1)
	return price, parcellist, dollars, priceNR, parcellistNR, dollarsNR

if __name__ == '__main__':
	price, parcellist, dollars, priceNR, parcellistNR, dollarsNR = calculatecheapest()
	csvReaderToScore.printResult(price, parcellist, dollars, priceNR, parcellistNR, dollarsNR)