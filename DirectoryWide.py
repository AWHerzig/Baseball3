import math
import names
import numpy


def pythag(a, b):  # A lot of this file is gonna be "just nice to have"
    return math.sqrt(a**2 + b**2)


def odds(chance):  # inputs are 0 to 1, default of uniform()
    X = numpy.random.uniform()
    if X < chance:
        return True
    else:
        return False


def quad(var, a, b, c):  # "just nice to have"
    return var**a + var*b + c


def polarDistance(R1, R2, A1, A2):  # Fielding is in polar coordinates, so distance to ball/base from spot needs this.
    return math.sqrt(R1**2 + R2**2 - 2*R1*R2*math.cos(A1-A2))


def lineDef(x, y):  # Defines the in-play lines... ok fine it switches back to cartesian but just for this i promise
    orig = -60 / math.sqrt(2)
    slope = (y - orig)/(x - orig)
    intercept = orig * (1 - slope)
    return [slope, intercept]


def polarToCartesian(r, A):  # Because ball position is defined in polar but in-play is cartesian
    x = r * math.cos(A)
    y = r * math.sin(A)
    return [x, y]


def clamp(val, low, high):  # nice2have, really surprised it isn't built-in Python
    if val < low:
        val = low
    elif val > high:
        val = high
    return val


def nameGen():  # Male for MLB realism but... I might get rid of it, I did for Baseball 2 iirc
    return names.get_full_name(gender='male')


def ageCurve(age, base=False):
    if base:
        if age < 5:
            return age-1
        elif age == 5:
            return 3
        else:
            return 8 - age
    else:
        if age < 5:
            return 1
        elif age == 5:
            return 0
        else:
            return -1


gravForce = -32.2  # in ft
mphTOfts = 1.467  # ft/s = 1.467 * mph
rubberToPlate = 60.5  # Pitcher's back foot is touching the rubber
split = .01  # How much time (sec) passes in between snapshots... kinda like a frame rate
bounceCo = .325  # This doesn't actually get used but someday it might
frictionDecel = -1.63  # Coefficient of Friction is .35... cuz I said so
SPstam = 50  # Gets added to/subtracted from based on game events, when 0 the P gets subbed
RPstam = 15  # Starters go longer than relievers
# [X-Accel, Y-Accel, Z-Velo, Baseline X, Baseline Y] baselines will be adjusted by Pitcher.
# This is for righties, lefties will flip Xs. Gravity gets added to Y-accel later
# SUUUPER Tentative... becoming less tentative
pitches = {'4SFB': [-2, 16, 90 * mphTOfts, -.3, 3], '2SFB': [-12, 4, 87 * mphTOfts, -.75, 2.5],
           '12-6': [2, -20, 75 * mphTOfts, 0, 1.5], 'SLID': [32, -8, 83 * mphTOfts, 1, 2],
           'CUT ': [12, -4, 85 * mphTOfts, .5, 2.7], 'SPLT': [-12, -8, 84 * mphTOfts, 0, 1.2],
           'SINK': [-6, 2, 89 * mphTOfts, 0, 2], 'SCRW': [-24, -16, 70 * mphTOfts, -.875, 1.2],
           'CHG ': [-12, -10, 81 * mphTOfts, -.5, 2]}

# Starting points (polar) for each position on any given play.
positions = {'P ': [55, math.pi/4], 'C ': [0, 0], '1B': [100, .05*math.pi],
             '2B': [110, .2*math.pi], '3B': [100, .45*math.pi], 'SS': [110, .3*math.pi],
             'LF': [270, .4*math.pi], 'CF': [285, .25*math.pi], 'RF': [270, .1*math.pi]}

# So index is equal to traditional notation, DH is 0 but who cares it never gets called.
posNotation = ['DH', 'P ', 'C ', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF']
hitterPos = list(positions.keys())[1:9]  # I think these are used for roster construction so a team doesn't get 13 LFs
infieldPos = list(positions.keys())[1:6]
outfieldPos = list(positions.keys())[6:9]

# These are based on the real values at the real stadiums... except the AllStar ones at the bottom I made those up
# RF, RCF, CF, LCF, LF to match angle value from ballInPlay(). Each represents 18 degrees of wall
# RCF and LCF are a little fudged sometimes for stadiums that don't have clean numbers, rest are just accurate
stadiums = {'WSN': [337, 377, 402, 370, 335], 'PHI': [329, 391, 401, 369, 330], 'ATL': [335, 385, 400, 375, 325],
            'NYM': [335, 375, 408, 385, 330], 'MIA': [344, 386, 400, 387, 335], 'CHC': [355, 368, 400, 368, 353],
            'STL': [336, 375, 400, 375, 335], 'CIN': [328, 379, 404, 370, 325], 'MIL': [344, 371, 400, 374, 345],
            'PIT': [325, 397, 399, 375, 320], 'LAD': [330, 370, 400, 370, 330], 'ARI': [330, 393, 407, 393, 334],
            'SFG': [339, 381, 391, 390, 309], 'SDP': [334, 374, 396, 387, 322], 'COL': [347, 390, 415, 375, 350],
            'NYY': [318, 399, 408, 385, 314], 'BOS': [310, 379, 390, 400, 302], 'BAL': [333, 386, 400, 373, 318],
            'TOR': [328, 375, 400, 375, 328], 'TBR': [315, 370, 404, 370, 322], 'CHW': [330, 375, 400, 375, 335],
            'MIN': [339, 395, 403, 367, 328], 'KCR': [330, 387, 410, 387, 330], 'CLE': [325, 370, 400, 393, 325],
            'DET': [345, 370, 420, 365, 330], 'HOU': [315, 383, 409, 390, 326], 'LAA': [347, 390, 396, 367, 350],
            'OAK': [330, 388, 400, 388, 330], 'SEA': [331, 378, 401, 381, 326], 'TEX': [329, 372, 407, 374, 326],
            'NLA': [350, 400, 420, 400, 350], 'ALA': [350, 400, 420, 400, 350]}


