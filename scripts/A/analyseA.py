import csv
import os.path
import random
import itertools
import sys
sys.path.append("..")
import main

def parcelNormalizer():
	""" Returns a ranking of the parcels by calculating a vector
		between the weight and the volume
	"""
	# Retrieve objects from the main.py
	cargoListId = main.createObjectsCargoList()

	# Creating the necessary lists obtained from the object
	nameList = [parcel for parcel in cargoListId]
	weightList = [cargoListId[parcel].weight for parcel in cargoListId]
	volumeList = [cargoListId[parcel].volume for parcel in cargoListId]

	# Calculating the sum of the 2 lists
	sumWL = sum(weightList)
	sumVL = sum(volumeList)

	# vectorize values of weight and volume
	weightList = [x/sumWL for x in weightList]
	volumeList = [x/sumVL for x in volumeList]
	vectorizedParcels = {}

	# Creating a dict containing vectorized values. Key: parcelId Value: vector
	for i in range(0,len(weightList)):
		vector = ((weightList[i]) + (volumeList[i]))/2
		vectorizedParcels[nameList[i]] = vector

	# Vectorized descending ranking of parcels, based on a combined variable between Weight and Volume
	ranking = sorted(vectorizedParcels,key=vectorizedParcels.get,reverse=True)
	return ranking

def shipNormalizer():
	""" Returns a ranking of the spacecrafts by calculating a vector
		between the weight and the volume
	"""
	# Retrieve objects from the main.py
	spaceCraftId = main.createObjectsSpaceCraft()

	# Creating the necessary lists obtained from the object
	nameList = [ship for ship in spaceCraftId]
	weightList = [spaceCraftId[ship].maxPayloadMass for ship in spaceCraftId]
	volumeList = [spaceCraftId[ship].maxPayload for ship in spaceCraftId]

	# Calculating the sum of the 2 lists
	sumWL = sum(weightList)
	sumVL = sum(volumeList)

	# vectorize values of weight and volume
	weightList = [x/sumWL for x in weightList]
	volumeList = [x/sumVL for x in volumeList]
	vectorizedShips = {}

	# Creating a dict containing vectorized values. Key: parcelId Value: vector
	for i in range(0,len(weightList)):
		vector = ((weightList[i]) + (volumeList[i]))/2
		vectorizedShips[nameList[i]] = vector

	# Vectorized descending ranking of ships, based on a combined variable between Weight and Volume
	ranking = sorted(vectorizedShips,key=vectorizedShips.get,reverse=True)
	return ranking

if __name__ == "__main__":
	cargoListId = main.createObjectsCargoList()
	# Creating the necessary lists obtained from the object
	nameList = [parcel for parcel in cargoListId]
	for x in nameList:
		if x not in parcelNormalizer():
			print(cargoListId[x].weight)
