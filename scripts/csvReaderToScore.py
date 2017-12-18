import sys
import main
import csv

def formatCostAsDollars(cost):
    """ Format cost to dollars to make it more readable """
    amount = str(cost)[:len(str(cost))-2]
    finalPriceFormatted = "$" + amount
    return finalPriceFormatted

def calculatescore(pathtofile, fueltype=1, cargolistnum=1, spacecraftfile=""):
    """Input: fueltype, bepaald of de daadwerkelijke waardes of de
       waarde 0,73 als fuel to weight gebruikt moet worden.
       Type 1 is daadwerkelijke waardes
       Type 2 is 0,73 voor alle
    """
    # Create spaceships and parcel objects
    spaceCraftId = main.createObjectsSpaceCraft(spacecraftfile)
    cargoListId = main.createObjectsCargoList(cargolistnum)

    # Read the csv file and make a list of lists out of it
    with open(pathtofile, 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = list(list(rec) for rec in csv.reader(csvfile, delimiter=','))

    # Every new attempt in the file seperates the data with a row "New attempt"
    # Because there is no data in it, we want to delete that row from the object
    for item in data:
        if item[0] == "New attempt":
            data.remove(item)

    spacecraftlist = [spacecraft for spacecraft in spaceCraftId.keys()]
    # Now merge 5 rows together, so every attempt is in its own list
    attemptlist = [data[x:x + len(spacecraftlist)+1] for x in range(0, len(data), len(spacecraftlist)+1)]
    print(attemptlist)
    # Initiate a bestcost and the item with the best cost
    bestList = []
    bestCost = 100000000000000000000000000
    count = 0

    # Get the highest score
    highest = 0
    if spacecraftfile == "DE":
        for item in attemptlist:
            if int(item[0][6]) > int(highest):
                highest = item[0][6]
    else:
        for item in attemptlist:
            if int(item[0][4]) > int(highest):
                highest = item[0][4]

    for item in attemptlist:
        if int(item[0][4]) == int(highest):
        # Reset the price and spacecrafts every new loop
            price = 0
            count += 1
            for spacecraft in spaceCraftId.keys():
                spaceCraftId[spacecraft].reset()

            # Add all the parcels from the precalculated lists to the spacecrafts
            for parcel in item[1]:
                spaceCraftId['Cygnus'].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
            for parcel in item[2]:
                spaceCraftId['Progress'].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
            for parcel in item[3]:
                spaceCraftId['Kounotori'].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
            for parcel in item[4]:
                spaceCraftId['Dragon'].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)

            if spacecraftfile == "DE":
                for parcel in item[5]:
                    spaceCraftId['TianZhou'].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
                for parcel in item[6]:
                    spaceCraftId['Verne ATV'].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)

            # Calculate the price
            if fueltype == 1:
                price += spaceCraftId['Cygnus'].calculateCost(spaceCraftId['Cygnus'].calculateFuel())
                price += spaceCraftId['Progress'].calculateCost(spaceCraftId['Progress'].calculateFuel())
                price += spaceCraftId['Kounotori'].calculateCost(spaceCraftId['Kounotori'].calculateFuel())
                price += spaceCraftId['Dragon'].calculateCost(spaceCraftId['Dragon'].calculateFuel())
                if spacecraftfile == "DE":
                    price += spaceCraftId['TianZhou'].calculateCost(spaceCraftId['TianZhou'].calculateFuel())
                    price += spaceCraftId['Verne ATV'].calculateCost(spaceCraftId['Verne ATV'].calculateFuel())

            if fueltype == 2:
                price += spaceCraftId['Cygnus'].calculateCost(spaceCraftId['Cygnus'].calculateFuel(0.73))
                price += spaceCraftId['Progress'].calculateCost(spaceCraftId['Progress'].calculateFuel(0.73))
                price += spaceCraftId['Kounotori'].calculateCost(spaceCraftId['Kounotori'].calculateFuel(0.73))
                price += spaceCraftId['Dragon'].calculateCost(spaceCraftId['Dragon'].calculateFuel(0.73))
                if spacecraftfile == "DE":
                    price += spaceCraftId['TianZhou'].calculateCost(spaceCraftId['TianZhou'].calculateFuel(0,73))
                    price += spaceCraftId['Verne ATV'].calculateCost(spaceCraftId['Verne ATV'].calculateFuel(0,73))

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

def printResult(price, parcellist, dollars, priceNR, parcellistNR, dollarsNR):
    print("<<< SUMMARY >>>")
    print("<<< RESULTS WITH FAKE FUEL TO WEIGHT VALUE >>>")
    print("Cygnus:", parcellistNR[0])
    print("Progress:", parcellistNR[1])
    print("Kounotori:", parcellistNR[2])
    print("Dragon:", parcellistNR[3])
    print("The lowest price found is: ", dollarsNR, "\n")

    print("<<< RESULTS WITH REAL FUEL TO WEIGHT VALUE >>>")
    print("Cygnus:", parcellist[0])
    print("Progress:", parcellist[1])
    print("Kounotori:", parcellist[2])
    print("Dragon:", parcellist[3])
    print("The lowest price found is: ", dollars)
    print("<<< Difference >>>")
    print("The difference is $", str(priceNR - price), "\n")


if __name__ == '__main__':
    # Get the information with the real fuel to weight values
    price, parcellist, dollars = calculatescore("A/record.csv", 1, 1)

    # Get the information with the fake fuel to weight values
    priceNR, parcellistNR, dollarsNR = calculatescore("A/record.csv", 2, 1)

    printResult(price, parcellist, dollars, priceNR, parcellistNR, dollarsNR)

