import main
spaceCraftId = main.createObjectsSpaceCraft()
cargoListId = main.createObjectsCargoList()

parcellist = [x for x in cargoListId.keys()]
for parcel in parcellist:
    # If there is room in the spacecraft, add the parcel
    if spaceCraftId["Cygnus"].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
        spaceCraftId["Cygnus"].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
        spaceCraftId["Cygnus"].addParcelToParcellist(parcel)

print(spaceCraftId["Cygnus"].parcellist)
lijstje = spaceCraftId["Cygnus"].parcellist
print ("lol", lijstje)
for i in list(lijstje):
	print (i)
	print (lijstje)
	spaceCraftId["Cygnus"].removeParcelFromParcellist(i)

print(spaceCraftId["Cygnus"].parcellist)

spaceCraftId["Cygnus"].addParcelToParcellist('CL1#5')
print(spaceCraftId["Cygnus"].parcellist)

spaceCraftId["Cygnus"].reset()
print(spaceCraftId["Cygnus"].parcellist)