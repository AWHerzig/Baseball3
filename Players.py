from DirectoryWide import *
import numpy
import random

# Values contract as length * (AAV**2)?  [2, 10] = 200, [1, 15] = 225


class Pitcher:
    def __init__(self, name, pos, hand=-1, top=11, controlled=False, test=False):
        self.name = name
        while len(self.name) > 15:  # To make statlines line up better, all names are same length
            self.name = nameGen()
        while len(self.name) < 15:
            self.name = self.name + ' '
        self.pos = pos
        self.secondary = numpy.NaN
        self.team = None
        self.cont = random.randrange(0, top)
        self.velo = random.randrange(0, top)
        self.move = random.randrange(0, top)
        self.field = random.randrange(0, top)
        self.speed = random.randrange(0, top)
        self.overall = self.cont + self.velo + self.move
        self.total = self.overall + self.field + self.speed
        if test:
            self.arsenal = ['4SFB', 'SLID', '12-6']
        else:
            self.arsenal = random.sample(list(pitches.keys()), k=3)  # They get 3 pitches for now it might change
        self.arStr = ''
        for i in self.arsenal:
            self.arStr = self.arStr + i[0:2]
        self.hand = hand  # -1 for right, 1 for left
        self.release = [hand, 6]  # Release width, height
        self.extension = numpy.random.normal(6.5, .5)
        self.available = True
        self.stamScore = 0
        self.usage = 0  # Consecutive games played
        self.age = random.randrange(1, 4)
        self.contract = [4-self.age, 2]
        self.controlled = controlled
        self.value = 0
        self.cost = 0
        self.offers = []
        self.saveOp = False  # Tag it to the player instead of the game so it can be decided fluidly? I think
        # Stats
        self.W = 0
        self.L = 0
        self.S = 0
        self.Hold = 0
        self.SO = 0
        self.OR = 0
        self.BF = 0
        self.ER = 0
        self.K = 0
        self.BB = 0
        self.HR = 0
        self.H = 0
        # calc Stats
        self.IP = 0
        self.ERA = 0
        self.WHIP = 0
        self.Kp = 0

    def __str__(self):
        return self.name

    def record(self):
        return '(' + str(self.W) + '-' + str(self.L) + ')'

    def calcStats(self):
        self.IP = round(self.OR / 3, 1)
        if self.IP > 0:
            self.ERA = round((self.ER * 9) / self.IP, 2)
            self.WHIP = round((self.H + self.BB) / self.IP, 2)
        if self.BF > 0:
            self.Kp = round(self.K / self.BF, 3)

    def smallLine(self):
        return self.name + '(' + str(self.age) + ';' + str(self.cont) + ',' + str(self.velo) + ',' + str(self.move) + ';' + str(round(self.ERA, 2)) + ')'

    def bigLine(self):
        return self.name + '(' + str(self.age) + ';' + str(self.cont) + ',' + str(self.velo) + ',' + str(self.move) \
               + ')' + str(self.IP) + 'IP, ' + self.record() + ', ' + str(self.S + self.Hold) + '/' + str(self.SO) + ' S+H, ' + \
               str(self.ERA) + 'ERA, ' + str(self.WHIP) + 'WHIP, ' + str(self.Kp) + 'K%'

    def canGetThere(self, dist, time):
        return dist < (17 + .5 * self.speed) * min(time - 1.1 + (.05*self.field), 0) + (1 + .5*self.field)

    def reset(self):  # Year to year reset
        self.available = True
        self.usage = 0
        self.OR = 0
        self.BF = 0
        self.ER = 0
        self.K = 0
        self.BB = 0
        self.HR = 0
        self.H = 0
        self.IP = 0
        self.ERA = 0
        self.WHIP = 0
        self.Kp = 0
        self.age += 1
        self.boost(ageCurve(self.age, self.controlled))
        self.contract[0] -= 1
        self.offers = []

    def boost(self, x):
        if self.controlled:
            self.cont += x
            self.velo += x
            self.move += x
            self.field += x
            self.speed += x
        else:
            self.cont += x
            self.velo += x
            self.move += x
            self.field += x
            self.speed += x
        self.overall = self.cont + self.velo + self.move
        self.total = self.overall + self.field + self.speed

    def acceptDeal(self):
        bestOffer = None
        bestValue = 0
        for i in self.offers:
            if i[1]*(i[2]**2) > bestValue:
                bestValue = i[1]*(i[2]**2)
                bestOffer = i
        if bestOffer is not None and self.pos == 'SP':
            bestOffer[0].rotation.loc[len(bestOffer[0].rotation)] = numpy.array([self, self.hand, self.arStr,
                                                                                 self.overall, self.extension], dtype=object)
            self.contract = bestOffer[1:3]
        elif bestOffer is not None and self.pos == 'RP':
            bestOffer[0].bullpen.loc[len(bestOffer[0].bullpen)] = numpy.array([self, self.hand, self.arStr,
                                                                               self.overall, self.extension, self.available], dtype=object)
            self.contract = bestOffer[1:3]
            self.team = bestOffer[0].ABR
        return bestOffer


class Hitter:
    def __init__(self, name, pos, hand=-1, top=11, controlled=False):
        self.name = name
        while len(self.name) > 15:  # To make statlines line up better, all names are same length
            self.name = nameGen()
        while len(self.name) < 15:
            self.name = self.name + ' '
        self.team = None
        self.pos = pos
        self.con = random.randrange(0, top)
        self.pow = random.randrange(0, top)
        self.vis = random.randrange(0, top)
        self.offense = self.con + self.pow + self.vis
        self.field = random.randrange(0, top)
        self.speed = random.randrange(0, top)
        self.overall = self.offense + self.field + self.speed
        self.hand = hand
        self.secondary = None
        self.outOfPos = False  # Defends worse
        self.available = True
        self.usage = 0  # Consecutive games played
        self.chargedTo = None
        self.age = random.randrange(1, 4)
        self.contract = [4 - self.age, 2]
        self.controlled = controlled
        self.value = 0
        self.cost = 0
        self.offers = []
        # Stats
        self.PA = 0
        self.H = 0
        self.BB = 0
        self.TB = 0
        self.HR = 0
        self.RBI = 0
        self.R = 0
        self.K = 0
        self.SB = 0
        self.CS = 0
        self.SF = 0
        self.zMissT = 0
        self.swings = 0
        # CalcStats
        self.AVG = 0
        self.OBP = 0
        self.SLG = 0
        self.OPS = 0
        self.Sp = 0
        self.zMissA = 0
        self.slash = ''
        self.BABIP = 0

    def __str__(self):
        return self.name

    def calcStats(self):
        if self.PA > 0:
            self.OBP = round((self.H + self.BB) / self.PA, 3)
        if self.PA - self.BB - self.SF > 0:
            self.AVG = round(self.H / (self.PA - self.BB - self.SF), 3)
            self.SLG = round(self.TB / (self.PA - self.BB - self.SF), 3)
            self.OPS = round(self.OBP + self.SLG, 3)
        if self.PA - self.BB - self.HR - self.K > 0:
            self.BABIP = round((self.H - self.HR) / (self.PA - self.BB - self.HR - self.K), 3)
        if self.SB + self.CS > 0:
            self.Sp = round(self.SB / (self.SB + self.CS), 3)
        if self.swings > 0:
            self.zMissA = round(self.zMissT / self.swings, 2)
        self.slash = str(self.AVG)[1:] + '/' + str(self.OBP)[1:] + '/' + str(self.SLG)

    def smallLine(self):
        return self.name + '(' + str(self.age) + ';' + str(self.vis) + ',' + str(self.con) + ',' + str(self.pow) + ';' + str(round(self.OPS, 2)) + ')'

    def bigLine(self):
        return self.name + '(' + str(self.age) + ';' + str(self.vis) + ',' + str(self.con) + ',' + str(self.pow) + ')' \
               + str(self.PA) + ' PA, ' + self.slash + ', ' + str(self.HR) + 'HR, ' + str(self.SB) + '/' + str(self.SB + self.CS) + \
               'SB, ' + str(self.RBI) + 'RBI'

    def canGetThere(self, dist, time):
        if self.outOfPos:
            return dist < (14 + .5 * self.speed) * (time - 2.4 + (.05*self.field)) + (self.field / 3)
        else:
            return dist < (17 + .5 * self.speed) * (time - 1.2 + (.05*self.field)) + (1 + .5*self.field)
            #return True

    def reset(self):
        self.PA = 0
        self.H = 0
        self.BB = 0
        self.TB = 0
        self.HR = 0
        self.RBI = 0
        self.R = 0
        self.K = 0
        self.SB = 0
        self.CS = 0
        self.SF = 0
        self.zMissT = 0
        self.swings = 0
        self.AVG = 0
        self.OBP = 0
        self.SLG = 0
        self.OPS = 0
        self.Sp = 0
        self.zMissA = 0
        self.slash = ''
        self.usage = 0
        self.available = True
        self.age += 1
        self.boost(ageCurve(self.age))
        self.contract[0] -= 1
        self.offers = []

    def boost(self, x):
        if self.controlled:
            self.con += x
            self.pow += x
            self.vis += x
            self.field += x
            self.speed += x
        else:
            self.con += x
            self.pow += x
            self.vis += x
            self.field += x
            self.speed += x
        self.offense = self.con + self.pow + self.vis
        self.overall = self.offense + self.field + self.speed

    def acceptDeal(self):
        bestOffer = None
        bestValue = 0
        for i in self.offers:
            if i[1]*(i[2]**2) > bestValue:
                bestValue = i[1]*(i[2]**2)
                bestOffer = i
        if bestOffer is not None:
            bestOffer[0].hitters.loc[len(bestOffer[0].hitters)] = numpy.array([self, self.pos, self.secondary, self.overall,
                                                                   self.offense, self.available], dtype=object)
            self.contract = bestOffer[1:3]
            self.team = bestOffer[0].ABR
        return bestOffer
