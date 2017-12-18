
import sys
sys.path.append("..")
import supportFunctionsHillClimber as supportHC
import main
import csv



if __name__ == '__main__':



def MakeTemporaryCargoList(oldCargolistId, filenameSendings, outputFilename,wantedShipment):
	sending = supportHC.openResults(oldCargolistId)[1][wantedShipment]
	CurrentCargoList = '../../data/' + outputFilename + '.csv'
	with open(CurrentCargoList, "w", newline='') as file:
		spamwriter = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerow(['parcel_ID','weight (kg)','volume (m^3)'])
		for item in sending:
			stats = []
			stats.append(item)
			stats.append(oldCargolistId[item].weight)
			stats.append(oldCargolistId[item].volume)
			spamwriter.writerow(stats)