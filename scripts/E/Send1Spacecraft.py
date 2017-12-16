import random
import itertools
import sys
sys.path.append("..")
import main
import csv

def send1Spacecraft():
    # Prepare spacecrafts and parcels
    spacecraftobject = main.createObjectsSpaceCraft("DE")
    cargoobject = main.createObjectsCargoList(3)

    tester = spacecraftobject['Cygnus']
    print ("HOII", tester.currentPayload)

    # Create a random order of parcels
    parcels = [parcel for parcel in cargoobject.keys()]

    generaldict = {}
    for spacecraft in spacecraftobject.keys():
        spacecraftname = spacecraft
        spacecraftdict = {}
        counter = 0
        print (len(parcels))
        if len(parcels)!= 0:
            counter += 1
            parcellist, dictrun = fillspacecraft(parcels, spacecraft, spacecraftobject, cargoobject)
            spacecraftdict[counter] = dictrun
            parcels = parcellist
        else:
            generaldict[spacecraft] = spacecraftdict

    return generaldict


def fillspacecraft(parcellist, spacecraft, spaceCraftId, cargoListId):
    # Create a copy of the parcellist, because you don't want to loop
    # through a list while you are removing items from that list
    copyparcel = [x for x in parcellist]

    space0 = []
    packetCount = 0
    for parcel in copyparcel:
        parcellist.remove(parcel)
        if spaceCraftId[spacecraft].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
            spaceCraftId[spacecraft].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
            space0.append(parcel)
            packetCount += 1
        else:
            parcellist.append(parcel)
            break;
    
    weight = spaceCraftId[spacecraft].currentPayloadMass
    volume = spaceCraftId[spacecraft].currentPayload
    price =  spaceCraftId[spacecraft].calculateCost(spaceCraftId[spacecraft].calculateFuel())
    returndict = {"weight":weight, "volume":volume, "Price": price}
    return parcellist, returndict

if __name__ == '__main__':
    print (send1Spacecraft())

