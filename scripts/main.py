import csv
import os.path
import random
import itertools
# open csv file with relative path
def readFile(relativePath):
    ''' Read csv file and return generator of information'''
    with open(relativePath) as csvfile:
        reader = csv.DictReader(csvfile)
        # Return information (as list to remove generator and not able to call)
        return list(reader)

# Class of spacecraft with parameters
class spaceCraft(object):
    # set default parameters
    nation = str
    organisation = str
    maxPayloadMass = float
    maxPayload = float
    mass = float
    baseCost = float
    fuelToWeight = float
    currentPayloadMass = 0
    currentPayload = 0

    # Used to create instance for itself if parameters are passed
    def __init__(self, Spacecraft, Nation, Organisation, PayloadMass,
                 Payload, Mass, BaseCost, fuelToWeight):
        self.spacecraft = Spacecraft
        self.nation = Nation
        self.organisation = Organisation
        self.maxPayloadMass = PayloadMass
        self.maxPayload = Payload
        self.mass = Mass
        self.baseCost = BaseCost
        self.fuelToWeight = fuelToWeight
        self.currentPayloadMass = 0
        self.currentPayload = 0

    def reset(self):
        ''' restore parameters from start
        '''
        self.currentPayloadMass = 0
        self.currentPayload = 0

    def checkFitCraft(self, parcelMass, parcelPayload):
        ''' Check if the parcel fits in the spacecraft.
            If yes: add, if no: notify
        '''
        if self.currentPayloadMass + parcelMass < self.maxPayloadMass and self.currentPayload + parcelPayload < self.maxPayload:
            return True

        elif self.currentPayloadMass + parcelMass > self.maxPayloadMass:
            #print ("To Heavy")
            return False

        elif self.currentPayload + parcelPayload > self.maxPayload:
            #print ("To Big")
            return False

    def addParcelToCraft(self, parcelMass, parcelPayload):
            # add parcel weigh and payload to spacecraft.
            self.currentPayloadMass = self.currentPayloadMass + parcelMass
            self.currentPayload = self.currentPayload + parcelPayload

    def calculateFuel(self, standardFuel=0):
        #(Mass + Payload-mass) x FtW / (1-FtW) = F
        if standardFuel == 0:
            standardFuel = self.fuelToWeight
        return round(self.mass + self.currentPayloadMass * self.fuelToWeight / (1-standardFuel), 2)

    def calculateCost(self,fuel):
        return self.baseCost + int(fuel*1000) * 5 

def createObjectsSpaceCraft():
    '''Create an instance of each parcel with Class cargoList '''
    # get the data for parcels from cvs
    spaceCraftCsv = readFile('../data/Spacecrafts.csv')

    # dict to store key value pair of name and class name.
    # Neceresary to make for loop work with instances.
    spaceCraftId = {}

    for row in spaceCraftCsv:
        # Convert each data entry to object of class Spacecraft
        # and parse parameters from csv to object
        spaceCraftId[str(row['Spacecraft'])] = spaceCraft(row['Spacecraft'],
                                                         row['Nation'],
                                                         row['Organisation'],
                                                         float(row['PayloadMass (kgs)']),
                                                         float(row['Payload (m3)']),
                                                         float(row['Mass (kgs)']),
                                                         float(row['BaseCost']),
                                                         float(row['Fuel-to-Weight'])
                                                         )
    # return dict to be able to find objects
    return spaceCraftId

# Class of cargo with parameters
class cargoList(object):
    # set default parameters
    cargoId = str
    weight = float
    volume = float

    # Used to create instance for itself if parameters are passed
    def __init__(self, Parcel_ID, Weight, Volume):
        self.cargoId = Parcel_ID
        self.weight = Weight
        self.volume = Volume

def createObjectsCargoList():
    '''Create an instance of each parcel with Class cargoList '''
    # get the data for parcels from cvs

    cargoListCsv = readFile('../data/CargoList1.csv')

    # dict to store key value pair of name and class name.
    # Neceresary to make for loop work with instances.
    cargoListId = {}

    for row in cargoListCsv:
        # Convert each data entry to object of class cargoList
        # and parse parameters from csv to object
        cargoListId[str(row['parcel_ID'])] = cargoList(row['parcel_ID'],
                                                         float(row['weight (kg)']),
                                                         float(row["volume (m^3)"])
                                                         )
    # return dict to be able to find objects
    return cargoListId

spaceCraftId = createObjectsSpaceCraft()
cargoListId = createObjectsCargoList()

### >> TESTCODE <<
print (spaceCraftId['Dragon'])
print (spaceCraftId['Dragon'].nation)
print (spaceCraftId['Cygnus'].organisation)
print (spaceCraftId['Cygnus'].spacecraft)
print ("===")
print (cargoListId['CL1#1'].weight)

    