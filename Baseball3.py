# X is across the plate, Y is Vertical, Z is distance to plate
# Ball is 2.86-2.94 inches diameter, im saying 3 in / .25 ft. Plate really 17 in, im saying 18 so 1.5 ft
# Means zone is -.875 to .875 in the X
# +X is to the right of the umpire, (0,0,0) is dead center plate
# Base Strike Zone will be 1.5 ft to 3.5 ft, but maybe will change off of batter height
# 60.5 ft from rubber to plate


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
from UserPlay import *
from Players import *
from DirectoryWide import *
from Testing import *

"""
#bigtest()
#bigtest2()
#bigtest3()
#bigtest4H()
#bigtest4P()
#bigtest5()
bigtest6()
"""
print('Values Key: [Contact, Power, Vision, Hitter Field/Speed, Control, Velocity, Movement, Pitcher Field/Speed]')
for j in Divisions:
    for i in j:
        print(i.name, 'values', i.values, 'with a budget of', i.budget)
    print()
year = 1
print('Loading rosters... (Ignore any warning lines)')
cur = pandas.DataFrame(columns=['Name', 'Pos1', 'Pos2', 'Age', 'Core', 'OVR', 'Value'])
while year <= 5:
    print(str(20*(year-1))+'%')
    holdovers = holdUpdate(cur)
    cur = offseason(year, 0, holdovers)
    year += 1
print('100%')
go = 'True'
offP = 1  # print value for the offseason
starter = userStartup()
#format2()
while go:
    if starter == '3':
        holdovers = holdUpdate(cur)
        cur = offseason(year, offP, holdovers)
        year += 1
    if schedLength in ['2', '162']:  # This is the kickoff for the whole thing
        playIt(schedule162)
    elif schedLength in ['0', '20']:
        playIt(schedule20)
    else:
        playIt(schedule52)
    holdovers = holdUpdate(cur)
    cur = offseason(year, offP, holdovers)
    year += 1
    go = input('Input anything to play another season, just hit enter to stop')
    #go = False
print('Thanks for playing :)')
# with pandas.ExcelWriter('Cscore_Pow_Res.xlsx') as writer:
#     testerDF.to_excel(writer)
#"""



