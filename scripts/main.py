import csv
import os.path

# open csv file with relative path
def readFile(relativePath):
    ''' Read csv file and return generator of information'''
    with open(os.path.dirname(__file__) + relativePath) as csvfile:
        reader = csv.DictReader(csvfile)
        # Return information (as list to remove generator and not able to call)
        return list(reader)
# Class of spacecraft with parameters
class spaceCraft(object):
    # set default parameters
    nation = str
    organisation = str
    payloadMass = float
    payload = float
    mass = float
    baseCost = int
    fuelToWeight = float

    # Used to create instance for itself if parameters are passed
    def __init__(self, Spacecraft, Nation, Organisation, PayloadMass,
                 Payload, Mass, BaseCost, fuelToWeight):
        self.spacecraft = Spacecraft
        self.nation = Nation
        self.organisation = Organisation
        self.payloadMass = PayloadMass
        self.payload = Payload
        self.mass = Mass
        self.baseCost = BaseCost
        self.fuelToWeight = fuelToWeight

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
                                                         row['PayloadMass (kgs)'],
                                                         row['Payload (m3)'],
                                                         row['Mass (kgs)'],
                                                         row['BaseCost'],
                                                         row['Fuel-to-Weight']
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
                                                         row['weight (kg)'],
                                                         row["volume (m^3)"]
                                                         )
    # return dict to be able to find objects
    return cargoListId

spaceCraftId = createObjectsSpaceCraft()
cargoListId = createObjectsCargoList()
### >> TESTCODE <<
# NOTES: voor python 3 haakjes om print, willen we daar rekening mee houden?
print (spaceCraftId['Dragon'])
print (spaceCraftId['Dragon'].nation)
print (spaceCraftId['Cygnus'].organisation)
print (spaceCraftId['Cygnus'].spacecraft)
print ("===")
print (cargoListId['CL1#1'].weight)
# MAAR dit mag bijvoorbeeld niet in classes
for craft in spaceCraftId.keys():
    # omdat ie nu gaat zoeken naar een instance van de class met de naam craft
    # ipv de variabele waar craft voor staat in de for loop
    print (spaceCraftId[craft].payload)

Cygnus = 0
CygnusVol = 0
Progress = 0
ProgressVol = 0
Kounotori = 0
KounotoriVol = 0
Dragon = 0
DragonVol = 0
CygLoad = []

for parcel in cargoListId.keys():
    print (cargoListId[parcel].weight, cargoListId[parcel].volume, cargoListId[parcel].cargoId)
    # 
    tempMass = (float(spaceCraftId['Cygnus'].fuelToWeight) * (Cygnus + float(spaceCraftId['Cygnus'].mass)))
    # Put the maximum weigth of the spacecraft Cygnus in a variable
    maxMassCygnus = (float(spaceCraftId['Cygnus'].payloadMass) + float(spaceCraftId['Cygnus'].mass))
    print tempMass, maxMassCygnus

    # Check of kg niet wordt overschreden als je toevoegt en daarna of payload niet
    if maxMassCygnus > (tempMass + float(cargoListId[parcel].weight)) and float(spaceCraftId['Cygnus'].payload) > (CygnusVol + float(cargoListId[parcel].volume)):
        # Verander huidige weigth
        Cygnus += float(cargoListId[parcel].weight)
        # Verander volume
        CygnusVol += float(cargoListId[parcel].volume)
        CygLoad.append(cargoListId[parcel].cargoId)

    # hier moet voor elke andere spacecraft
print CygLoad
