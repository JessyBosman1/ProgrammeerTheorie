import csv
import os.path
import random
import itertools
import main
import analyseA

spaceCraftId = main.createObjectsSpaceCraft()
cargoListId = main.createObjectsCargoList()
spaceCraftRank = ["Cygnus"]
parcelRank = analyseA.parcelNormalizer()
final={}
RemoveParcels=[]
for ship in reversed(spaceCraftRank):
	lowestMass=0
	amount = 0
	results={}
	winner=[]
	while(amount<250000):
		if amount%50000==0:
			print (amount)
		options=True
		strikes=0
		if len(RemoveParcels)==0:
			parcelRank = analyseA.parcelNormalizer()
		else:
			parcelRank = analyseA.parcelNormalizer()
			for x in RemoveParcels:
				parcelRank.remove(x)
		spaceCraftId[ship].reset()
		usedPackets=[]
		while(options):
			if strikes==100:
				options=False
			else:
				parcel=random.choice(parcelRank)
				if spaceCraftId[ship].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
					spaceCraftId[ship].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
					usedPackets.append(parcel)
					parcelRank.remove(parcel)

				else:
					strikes+=1
		results[amount]=[usedPackets,len(usedPackets),round(spaceCraftId[ship].currentPayload/spaceCraftId[ship].maxPayload*100,4), round(spaceCraftId[ship].currentPayloadMass/spaceCraftId[ship].maxPayloadMass*100,4)]
		if lowestMass<results[amount][1]:
			lowestMass=results[amount][1]
			winner=[usedPackets,len(usedPackets),round(spaceCraftId[ship].currentPayload/spaceCraftId[ship].maxPayload*100,4), round(spaceCraftId[ship].currentPayloadMass/spaceCraftId[ship].maxPayloadMass*100,4)]
			parcelsToRemove=[]
			print (lowestMass, winner[2], winner[3], winner[0])
			for par in usedPackets:
				parcelsToRemove.append(par)
		amount+=1
	final[ship]=winner
	for x in parcelsToRemove:
		RemoveParcels.append(x)
	parcelsToRemove=[]
total=0
for x in final:
	print (x, final[x])
	total+=final[x][1]
print (total)







def firstTry():
	spaceCraftId = main.createObjectsSpaceCraft()
	cargoListId = main.createObjectsCargoList()
	spaceCraftRank = analyseA.shipNormalizer()
	parcelRank = analyseA.parcelNormalizer()
	parcelsCompleted = []
	for ship in reversed(spaceCraftRank):
		amountOfParcels = 0
		optionsLeft = True
		for parcel in reversed(parcelRank):
			if optionsLeft:
				#first attempt
				if spaceCraftId[ship].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
					spaceCraftId[ship].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
					parcelsCompleted.append(parcel)
					parcelRank.remove(parcel)
					amountOfParcels += 1;
				else:
					#second attempt
					for other_parcel in parcelRank:
						if spaceCraftId[ship].addParcelToCraft(cargoListId[other_parcel].weight, cargoListId[other_parcel].volume) != False:
							spaceCraftId[ship].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
							parcelsCompleted.append(parcel)
							parcelRank.remove(parcel)
							amountOfParcels += 1
						else:
							optionsLeft = False

		print (ship)
		print ("Parcels in this ship:", amountOfParcels)
		print ("Room left: ",spaceCraftId[ship].maxPayload-spaceCraftId[ship].currentPayload, " m^3 and ",spaceCraftId[ship].maxPayloadMass-spaceCraftId[ship].currentPayloadMass," kg")
		print (parcelsCompleted, len(parcelsCompleted))

