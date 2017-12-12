import sys
sys.path.append("..")
sys.path.append("../A")
import main
import csv

def formatCostAsDollars(cost):
	""" Format cost to dollars to make it more readable	"""
	amount = str(cost)[:len(str(cost))-2]
	finalPriceFormatted = "$" + amount
	return finalPriceFormatted

def calculatescore(fueltype=1):
	"""Input: fueltype, bepaald of de daadwerkelijke waardes of de
	   waarde 0,73 als fuel to weight gebruikt moet worden.
	   Type 1 is daadwerkelijke waardes
	   Type 2 is 0,73 voor alle"""
	# Create spaceships and parcel objects
	spaceCraftId = main.createObjectsSpaceCraft()
	cargoListId = main.createObjectsCargoList()

	# Read the csv file and make a list of lists out of it
	with open("../A/random1Attempt_100x_1000000_20_5.csv") as csvfile:
		reader = csv.reader(csvfile)
		data = list(list(rec) for rec in csv.reader(csvfile, delimiter=','))

	# Every new attempt in the file seperates the data with a row "New attempt"
	# Because there is no data in it, we want to delete that row from the object
	for item in data:
		if item[0] == "New attempt":
			data.remove(item)

	# Now merge 5 rows together, so every attempt is in its own list
	attemptlist = [data[x:x+5] for x in range(0, len(data), 5)]

	# Initiate a bestcost and the item with the best cost
	bestList = []
	bestCost = 100000000000000000000000000
	count = 0

	for item in attemptlist:
		# Reset the price and spacecrafts every new loop
		price = 0
		count += 1
		spaceCraftId['Progress'].reset()
		spaceCraftId['Cygnus'].reset()
		spaceCraftId['Kounotori'].reset()
		spaceCraftId['Dragon'].reset()

		# Add all the parcels from the precalculated lists to the spacecrafts
		for parcel in item[1]:
			spaceCraftId['Cygnus'].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
		for parcel in item[2]:
			spaceCraftId['Progress'].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
		for parcel in item[3]:
			spaceCraftId['Kounotori'].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
		for parcel in item[4]:
			spaceCraftId['Dragon'].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)

		# Calculate the price
		if fueltype == 1:
			price += spaceCraftId['Cygnus'].calculateCost(spaceCraftId['Cygnus'].calculateFuel(0.73))
			price += spaceCraftId['Progress'].calculateCost(spaceCraftId['Progress'].calculateFuel(0.74))
			price += spaceCraftId['Kounotori'].calculateCost(spaceCraftId['Kounotori'].calculateFuel(0.71))
			price += spaceCraftId['Dragon'].calculateCost(spaceCraftId['Dragon'].calculateFuel(0.72))

		if fueltype == 2:
			price += spaceCraftId['Cygnus'].calculateCost(spaceCraftId['Cygnus'].calculateFuel(0.73))
			price += spaceCraftId['Progress'].calculateCost(spaceCraftId['Progress'].calculateFuel(0.73))
			price += spaceCraftId['Kounotori'].calculateCost(spaceCraftId['Kounotori'].calculateFuel(0.73))
			price += spaceCraftId['Dragon'].calculateCost(spaceCraftId['Dragon'].calculateFuel(0.73))

		# If the price is lower than the current best cost, make it the new best cost
		if price < bestCost:
			bestCost = price
			dollars = formatCostAsDollars(price)
			bestList = item
			print ("<<< NEW CHEAPEST >>>")
			print ("<<< THE INFO: >>>")
			for y in spaceCraftId.keys():
				print(y)
				print ("Payload (current, max)", spaceCraftId[y].currentPayload, spaceCraftId[y].maxPayload,
				str(round(spaceCraftId[y].currentPayload / spaceCraftId[y].maxPayload * 100, 2)) + "%")
				print ("PayloadMass (current, max)", spaceCraftId[y].currentPayloadMass, spaceCraftId[y].maxPayloadMass, 
				str(round(spaceCraftId[y].currentPayloadMass / spaceCraftId[y].maxPayloadMass * 100, 2)) + "%")
			print ("<<< $$$$$$$ >>>")
			print ("Best cost is: ", dollars, " at count ", count)

	return bestCost, bestList, dollars

