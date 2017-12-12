import sys
sys.path.append("..")
sys.path.append("../A")
import main
import csv
import csvReaderToScore

# Get the information with the real fuel to weight values
price, parcellist, dollars = csvReaderToScore.calculatescore(1)

# Get the information with the fake fuel to weight values
priceNR, parcellistNR, dollarsNR = csvReaderToScore.calculatescore(2)

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
print("The difference is $", price - priceNR)