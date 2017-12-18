import random
import itertools
import os
import sys
sys.path.append("..")
import main
import preparation
import csv
import supportFunctionsHillClimber as supportHC

def logicalSolution():
    """ Greedy algorithm that calculates the percentage of weight and volume
        that is used after adding a parcel. If more weight than volume is filled,
        it tries to fit packets with an higher weight first and the other way around
    """
    spaceCraftId = main.createObjectsSpaceCraft()
    cargoListId = main.createObjectsCargoList()
    spaceList = [ship for ship in spaceCraftId]

    # Shuffles the ships
    shuffleGen = itertools.permutations(spaceList, len(spaceList))
    shuffleList = [x for x in shuffleGen]

    maxScore = 79
    attempt = {}
    # Loop through all the permutations
    for spacelist in shuffleList:
        total = 0
        done = []
        attempt[spacelist] = {}

        # Loop through each ship
        for ship in spacelist:
            spaceCraftId[ship].reset()
            cargo = {}

            # Change this number to choose the prefered sorting mechanism
            # 1: vector, 2: volume 3: weight
            chosen, volumeList, weightList = preparation.top50Maker(1)

            # Remove already added parcels
            for x in done:
                if x in chosen:
                    chosen.remove(x)
                    volumeList.remove(x)
                    weightList.remove(x)

            # Loops through all the parcels
            for x in range(0, len(chosen)):

                # Finds the optimal parcel
                parcel, symbol = preparation.findSpace(spaceCraftId, ship, chosen, volumeList, weightList)

                # Checks if the parcel fits
                if spaceCraftId[ship].checkFitCraft(cargoListId[parcel].weight, cargoListId[parcel].volume) != False:
                    spaceCraftId[ship].addParcelToCraft(cargoListId[parcel].weight, cargoListId[parcel].volume)
                    cargo[parcel] = symbol
                    done.append(parcel)

                # Remove this parcel, added or not, from the list
                chosen.remove(parcel)
                volumeList.remove(parcel)
                weightList.remove(parcel)

            # Collects the attempts
            attempt[spacelist][ship] = cargo
            total += len(cargo)

        # Checks for highscores
        if total >= maxScore:
            maxScore = total
            for y in spacelist:
                print (y, attempt[spacelist][y])
                print ("Payload (current, max)", spaceCraftId[y].currentPayload, spaceCraftId[y].maxPayload,
                       str(round(spaceCraftId[y].currentPayload / spaceCraftId[y].maxPayload * 100, 2)) + "%")
                print ("PayloadMass (current, max)", spaceCraftId[y].currentPayloadMass, spaceCraftId[y].maxPayloadMass,
                       str(round(spaceCraftId[y].currentPayloadMass / spaceCraftId[y].maxPayloadMass * 100, 2)) + "%")
                print (len(attempt[spacelist][y]))
                print ('---------------')

            print (total)
            print ('---------------')

    print (maxScore)

    filename = "solutionA.csv"
    path = "savedResults"
    fullpath = os.path.join(path, filename)

    supportHC.getBestRun(attempt, spaceList, fullpath,cargoListId, spaceCraftId, True)

if __name__ == "__main__":
    logicalSolution()
