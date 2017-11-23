import main
import random
import itertools


def parcelNormalizer(type):
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

	input=volumeList
	if type==2:
		input=volumeList
	elif type==3:
		input=weightList

	# Creating a dict containing vectorized values. Key: parcelId Value: vector
	for i in range(0,len(input)):
		if type!=1:
			vector = (input[i])
		else:
			vector = ((weightList[i]) + (volumeList[i]))/2
		vectorizedParcels[nameList[i]] = vector

	# Vectorized descending ranking of parcels, based on a combined variable between Weight and Volume
	ranking = sorted(vectorizedParcels,key=vectorizedParcels.get,reverse=False)
	return ranking

# Checks if which is more available: volume or weight if these are the same it chooses the main chosen ranking
def findSpace(spaceCrafts,ship, chosen, weightList, volumeList):
	volumeLeft = spaceCraftId[ship].currentPayload/spaceCraftId[ship].maxPayload*100.0
	weightLeft = spaceCraftId[ship].currentPayloadMass/spaceCraftId[ship].maxPayloadMass*100.0

	if volumeLeft < weightLeft:
		return volumeList[0], "v"
	elif volumeLeft > weightLeft:
		return weightList[0], "w"
	else:
		return chosen[0], "p"

# Makes sure that all the lists contain the samen values as the top50
def shortlistMaker(top50, toShorten):
	result = []
	for x in toShorten:
		if x in top50:
			result.append(x)
	return result

# 1: vector, 2: volume 3: weight
def top50Maker(preference):
	if preference == 1:
		top50 = parcelNormalizer(1)#[:50]
		parcelRankVol = shortlistMaker(top50, parcelNormalizer(2))
		parcelRankWeight = shortlistMaker(top50, parcelNormalizer(3))
		return top50, parcelRankVol, parcelRankWeight
	elif preference == 2:
		top50 = parcelNormalizer(2)#[:50]
		parcelRankVol = shortlistMaker(top50, parcelNormalizer(2))
		parcelRankWeight = shortlistMaker(top50, parcelNormalizer(3))
		return top50, parcelRankVol, parcelRankWeight
	else:
		top50 = parcelNormalizer(3)#[:50]
		parcelRankVol = shortlistMaker(top50, parcelNormalizer(2))
		parcelRankWeight = shortlistMaker(top50, parcelNormalizer(3))
		return top50, parcelRankVol, parcelRankWeight

spaceCraftId = main.createObjectsSpaceCraft()
cargoListId = main.createObjectsCargoList()
nameList = [ship for ship in spaceCraftId]

#shuffles the ships
spaceList = ['Progress', 'Cygnus', 'Kounotori', 'Dragon']
shuffleGen = itertools.permutations(spaceList, len(spaceList))
shuffleList = [x for x in shuffleGen]

maxScore = 79
lowPrice = [];
attempt = {}

#loop through all the permutations
for spacelist in shuffleList:
	total = 0
	price = 0
	done = []
	attempt[spacelist] = {}

	#loop through each ship
	for ship in spacelist:
		spaceCraftId[ship].reset()
		cargo = {}

		# Change this number to choose the prefered sorting mechanism
		chosen, volumeList, weightList = top50Maker(1)

		#remove already added parcels
		for x in done:
			if x in chosen:
				chosen.remove(x)
				volumeList.remove(x)
				weightList.remove(x)

		#loops through all the parcels
		for x in range(0,len(chosen)):
			#finds the optimal parcel
			parcel,symbol = findSpace(spaceCraftId, ship, chosen, volumeList, weightList)

			#checks if the parcel fits
			if spaceCraftId[ship].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
				spaceCraftId[ship].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
				cargo[parcel] = symbol
				done.append(parcel)

			#remove this parcel, added or not, from the list
			chosen.remove(parcel)
			volumeList.remove(parcel)
			weightList.remove(parcel)
		price += spaceCraftId[ship].calculateCost(spaceCraftId[ship].calculateFuel(0.73))

		#collects the attempts
		attempt[spacelist][ship] = [cargo,price]
		total += len(cargo)

	#checks for highscores
	if total >= maxScore:
		if total > maxScore:
			lowPrice = []
			lowPrice.append(price)
			maxScore = total
		elif total == maxScore:
			lowPrice.append(price)

		for y in spacelist:
			print (y, attempt[spacelist][y][0])
			print ("Payload (current, max)", spaceCraftId[y].currentPayload,
					spaceCraftId[y].maxPayload,
					str(round(spaceCraftId[y].currentPayload/spaceCraftId[y].maxPayload*100, 2))+"%")

			print ("PayloadMass (current, max)", spaceCraftId[y].currentPayloadMass,
					spaceCraftId[y].maxPayloadMass,
					str(round(spaceCraftId[y].currentPayloadMass/spaceCraftId[y].maxPayloadMass*100, 2))+"%")

			print (len(attempt[spacelist][y][0]) , attempt[spacelist][y][1])
			print ('---------------')

		print (total, price)
		print ('---------------')

def formatCostAsDollars(cost):
	""" Format cost to dollars	"""
	amount = str(cost)[:len(str(cost))-2]
	finalPriceFormatted = "$" + amount
	return finalPriceFormatted

print ("Max " + str(maxScore) + " parcels; with a price of = " + formatCostAsDollars(min(lowPrice)))
print ("")
