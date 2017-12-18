import csv
import os.path
import random
import itertools
import sys
sys.path.append("..")
import main
import analyseA
import time
starttime = time.time()

def vectorBasedA(numberofloops):
	""" Tries to fill the spacecraft by choosing packets that
		match the vector of the spacecraft itself
	"""
	# Create objects
	spaceCraftId = main.createObjectsSpaceCraft()
	cargoListId = main.createObjectsCargoList()

	# Rank the ships and parcels
	spaceCraftRank = analyseA.shipNormalizer()
	parcelRank = analyseA.parcelNormalizer()

	# Remove heaviest parcels
	parcelRank.remove("CL1#58")
	parcelRank.remove("CL1#34")
	parcelRank.remove("CL1#83")
	final={}
	RemoveParcels=[]

	# Add parcels to ship
	for ship in reversed(spaceCraftRank):
		lowestMass = 0
		amount = 0
		results = {}
		winner = []

		while(amount < numberofloops):
			options = True
			strikes = 0

			# Generate the parcel rank and create an updated version without usedParcels
			if len(RemoveParcels) == 0:
				parcelRank = analyseA.parcelNormalizer()
			else:
				parcelRank = analyseA.parcelNormalizer()
				for x in RemoveParcels:
					parcelRank.remove(x)

			# Resets the ship, so it could be tested once again
			spaceCraftId[ship].reset()
			usedPackets = []

			# This will try 
			while(options):
				if strikes == 10:
					options = False
				else:
					parcel = random.choice(parcelRank)
					parcelRank.remove(parcel)
					# Checks if the parcel fits
					if spaceCraftId[ship].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
						spaceCraftId[ship].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
						usedPackets.append(parcel)
					else:
						# It will be punished if it won't fit
						strikes += 1
			results[amount] = [usedPackets,len(usedPackets),round(spaceCraftId[ship].maxPayload-spaceCraftId[ship].currentPayload,4), round(spaceCraftId[ship].maxPayloadMass-spaceCraftId[ship].currentPayloadMass,4)]
			# Gets the best score
			if lowestMass < results[amount][3]:
				lowestMass = results[amount][3]
				winner = [usedPackets,len(usedPackets),round(spaceCraftId[ship].maxPayload-spaceCraftId[ship].currentPayload,4), round(spaceCraftId[ship].maxPayloadMass-spaceCraftId[ship].currentPayloadMass,4)]
				parcelsToRemove = []
				for par in usedPackets:
					parcelsToRemove.append(par)
			amount += 1
		final[ship] = winner
		
		for x in parcelsToRemove:
			RemoveParcels.append(x)
		parcelsToRemove = []
	
	total = 0
	
	for x in final:
		print (x, final[x])
		total += final[x][1]
	print(total)

	# Print information for user
	for y in spaceCraftId.keys():
		print(y)
		print ("Payload (current, max)", spaceCraftId[y].currentPayload, spaceCraftId[y].maxPayload,
			str(round(spaceCraftId[y].currentPayload / spaceCraftId[y].maxPayload * 100, 2)) + "%")
		print ("PayloadMass (current, max)", spaceCraftId[y].currentPayloadMass, spaceCraftId[y].maxPayloadMass, 
			str(round(spaceCraftId[y].currentPayloadMass / spaceCraftId[y].maxPayloadMass * 100, 2)) + "%")
	endtime = time.time()
	print("Tijd: ", endtime - starttime)	

if __name__ == '__main__':
	vectorBasedA(25000);
