import os.path
import random
import itertools
import sys
sys.path.append("..")
sys.path.append("../A")
import main
import randomA

# This code simply gets the random code from A and runs it on cargolist 2
if __name__ == '__main__':
    randomA.randomAlgorithm(1000000, 80, 60, 2)