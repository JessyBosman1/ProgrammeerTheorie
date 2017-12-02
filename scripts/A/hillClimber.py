import random
import itertools
import sys
sys.path.append("..")
import main
import SolutionA
import csv


spaceCraftId = main.createObjectsSpaceCraft()
cargoListId = main.createObjectsCargoList()


def openResults(filename):
	"""Haalt de attempt op uit een csv-bestand en returnt de spacelist
	 en de verdeling"""
	with open(filename, "r") as file:
		reader = csv.reader(file)
		dividedParcels = list(reader)

	spaceList = dividedParcels[0]
	dividedParcels = dividedParcels[1:]
	return spaceList, dividedParcels

def getParcels(dividedParcels):
	"""Vind alle ontbekende parcels die niet in de schepen zitten en returnt
	deze samen met een lijst van alle gebruikte parcels"""
	usedParcels = [parcel for ship in dividedParcels for parcel in ship]
	unusedParcels = [parcel for parcel in cargoListId if parcel not in usedParcels]
	return usedParcels, unusedParcels

def prepareSpaceCrafts(spaceList, dividedParcels):
	"""Maakt de schepen klaar om mee te testen"""
	for ship in range(0,len(spaceList)):
		shipName = spaceList[ship]
		spaceCraftId[shipName].reset()
		for parcel in dividedParcels[ship]:
			spaceCraftId[shipName].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)



print(getParcels(openResults("attempt1.csv")[1]))