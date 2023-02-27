# X is across the plate, Y is Vertical, Z is distance to plate
# Ball is 2.86-2.94 inches diameter, im saying 3 in / .25 ft. Plate really 17 in, im saying 18 so 1.5 ft
# Means zone is -.875 to .875 in the X
# +X is to the right of the umpire, (0,0,0) is dead center plate
# Base Strike Zone will be 1.5 ft to 3.5 ft, but maybe will change off of batter height
# 60.5 ft from rubber to plate

from inputimeout import inputimeout
from matplotlib import pyplot as plt
import random
import numpy
import datetime
import math
import time
import pandas

from Gameplay import *
from Team import *
from League import *
from Team import *
from Players import *
from DirectoryWide import *


def bigtest():  # Each level of hitter plays each level of pitcher and returns some stat, usually ERA or OPS
    testing = pandas.DataFrame(columns=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
    for i in range(11):
        print('Round', i)
        testing.loc[len(testing)] = [test(i, j) for j in range(11)]
    print('hitter is row, pitcher is column')
    print(testing)


def bigtest2(p=5):  # Each level of hitter plays specific level of pitcher and returns full outcome breakdown
    testing = pandas.DataFrame(columns=['K', 'BB', 'HR', 'S', 'D', 'T', 'IPHR', 'Outs', 'OBP', 'SLG'])
    for i in range(11):
        testing.loc[len(testing)] = test2(i, p)
    print('hitter is row, pitcher is', p)
    print(testing)


#for i in range(11):
    #bigtest2(i)
#bigtest()
#bigtest()


if schedLength in ['', '52', '1']:  # This is the kickoff for the whole thing
    playIt(schedule52)
elif schedLength in ['0', '20']:
    playIt(schedule20)
elif schedLength in ['2', '162']:
    playIt(schedule162)
else:
    print('whoopsie')