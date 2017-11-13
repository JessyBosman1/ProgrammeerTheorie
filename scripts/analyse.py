import csv
import os.path
import random
import itertools
import main

def parcelNormalizer():
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
	ranking = sorted(vectorizedParcels,key=vectorizedParcels.get,reverse=True)[:97]
	return ranking

def shipNormalizer():
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
print parcelNormalizer()
print
print shipNormalizer()