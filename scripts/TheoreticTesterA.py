import main
import analyseA
import random



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


def findSpace(spaceCrafts,ship, chosen, weightList, volumeList):
	volumeLeft=spaceCraftId[ship].currentPayload/spaceCraftId[ship].maxPayload*100.0
	weightLeft=spaceCraftId[ship].currentPayloadMass/spaceCraftId[ship].maxPayloadMass*100.0
	if volumeLeft<weightLeft:
		return volumeList[0],"v"
	elif volumeLeft>weightLeft:
		return weightList[0],"w"

	else:
		return chosen[0],"p"

def shortlistMaker(top50, toShorten):
	result=[]
	for x in toShorten:
		if x in top50:
			result.append(x)
	return result

# 1: vector, 2: volume 3: weight
def top50Maker(preference):
	if preference==1:
		top50=parcelNormalizer(1)#[:50]
		parcelRankVol = shortlistMaker(top50,parcelNormalizer(2))
		parcelRankWeight = shortlistMaker(top50,parcelNormalizer(3))	
		return top50, parcelRankVol, parcelRankWeight
	elif preference==2:
		top50=parcelNormalizer(2)#[:50]
		parcelRankVol = shortlistMaker(top50,parcelNormalizer(2))
		parcelRankWeight = shortlistMaker(top50,parcelNormalizer(3))
		return top50, parcelRankVol, parcelRankWeight
	else:
		top50=parcelNormalizer(3)#[:50]
		parcelRankVol = shortlistMaker(top50,parcelNormalizer(2))
		parcelRankWeight = shortlistMaker(top50,parcelNormalizer(3))
		return top50, parcelRankVol, parcelRankWeight



spaceCraftId = main.createObjectsSpaceCraft()
cargoListId = main.createObjectsCargoList()
nameList = [ship for ship in spaceCraftId]
total=0
for ship in nameList:
	spaceCraftId[ship].reset()
	cargo={}
	# Change this number to choose the prefered sorting mechanism
	chosen, volumeList, weightList = top50Maker(2)
	for x in range(0,len(chosen)):
		parcel,symbol = findSpace(spaceCraftId,ship, chosen, volumeList,weightList)
		if spaceCraftId[ship].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
			spaceCraftId[ship].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
			cargo[parcel]=symbol
		chosen.remove(parcel)
		volumeList.remove(parcel)
		weightList.remove(parcel)
	print (ship, len(cargo))
	print (cargo)
	print ("Payload (current, max)", spaceCraftId[ship].currentPayload, spaceCraftId[ship].maxPayload, str(round(spaceCraftId[ship].currentPayload/spaceCraftId[ship].maxPayload*100,2))+"%")
	print ("PayloadMass (current, max)", spaceCraftId[ship].currentPayloadMass, spaceCraftId[ship].maxPayloadMass, str(round(spaceCraftId[ship].currentPayloadMass/spaceCraftId[ship].maxPayloadMass*100,2))+"%")
	print ('---------------')
	total+=len(cargo)
print(total)



