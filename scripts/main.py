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
    '''Create an instance of each spacecrafts with Class spaceCraft '''
    # get the data for spacecrafts from cvs
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

spaceCraftId = createObjectsSpaceCraft()

### >> TESTCODE <<
# NOTES: voor python 3 haakjes om print, willen we daar rekening mee houden?
print (spaceCraftId['Dragon'])
print (spaceCraftId['Dragon'].nation)
print (spaceCraftId['Cygnus'].organisation)
print (spaceCraftId['Cygnus'].spacecraft)
print ("===")
# MAAR dit mag bijvoorbeeld niet in classes
for craft in spaceCraftId.keys():
    # omdat ie nu gaat zoeken naar een instance van de class met de naam craft
    # ipv de variabele waar craft voor staat in de for loop
    (spaceCraftId[craft].spacecraft)
