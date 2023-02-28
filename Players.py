from DirectoryWide import *
import numpy
import random


class Pitcher:
    def __init__(self, name, pos, hand=-1, controlled=False):
        self.name = name
        while len(self.name) > 15:  # To make statlines line up better, all names are same length
            self.name = nameGen()
        while len(self.name) < 15:
            self.name = self.name + ' '
        self.pos = pos
        self.team = None
        self.cont = random.randrange(0, 11)
        self.velo = random.randrange(0, 11)
        self.move = random.randrange(0, 11)
        self.field = random.randrange(0, 11)
        self.speed = random.randrange(0, 11)
        self.overall = self.cont + self.velo + self.move
        self.total = self.overall + self.field + self.speed
        self.arsenal = random.sample(list(pitches.keys()), k=3)  # They get 3 pitches for now it might change
        self.hand = hand  # -1 for right, 1 for left
        self.release = [hand, 6]  # Release width, height
        self.extension = numpy.random.normal(6.5, .5)
        self.available = True
        self.stamScore = 0
        self.usage = 0  # Consecutive games played
        self.age = random.randrange(1, 5)
        self.contract = [4-self.age if self.age < 4 else 6-age, 10]
        self.controlled = controlled
        # Stats
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

    def calcStats(self):
        self.IP = round(self.OR / 3)
        if self.IP > 0:
            self.ERA = round((self.ER * 9) / self.IP, 2)
            self.WHIP = round((self.H + self.BB) / self.IP, 2)
        if self.BF > 0:
            self.Kp = round(self.K / self.BF, 3)

    def smallLine(self):
        return self.name + '(' + str(self.cont) + ',' + str(self.velo) + ',' + str(self.move) + ';' + str(round(self.ERA, 2)) + ')'

    def canGetThere(self, dist, time):
        return dist < (20 + self.speed) * (time-1.5 + (.1*self.field)) + (self.field / 2)

    def reset(self):  # Year to year reset
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


class Hitter:
    def __init__(self, name, pos,  hand=-1, controlled=False):
        self.name = name
        while len(self.name) > 15:  # To make statlines line up better, all names are same length
            self.name = nameGen()
        while len(self.name) < 15:
            self.name = self.name + ' '
        self.team = None
        self.pos = pos
        self.con = random.randrange(0, 11)
        self.pow = random.randrange(0, 11)
        self.vis = random.randrange(0, 11)
        self.offense = self.con + self.pow + self.vis
        self.field = random.randrange(0, 11)
        self.speed = random.randrange(0, 11)
        self.overall = self.offense + self.field + self.speed
        self.hand = hand
        self.secondary = None
        self.outOfPos = False  # Defends worse
        self.available = True
        self.usage = 0  # Consecutive games played
        self.chargedTo = None
        self.age = random.randrange(1, 5)
        self.contract = [4 - self.age if self.age < 4 else 6 - age, 10]
        self.controlled = controlled
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

    def __str__(self):
        return self.name

    def calcStats(self):
        if self.PA > 0:
            self.OBP = round((self.H + self.BB) / self.PA, 3)
        if self.PA - self.BB > 0:
            self.AVG = round(self.H / (self.PA - self.BB), 3)
            self.SLG = round(self.TB / (self.PA - self.BB), 3)
            self.OPS = round(self.OBP + self.SLG, 3)
        if self.SB + self.CS > 0:
            self.Sp = round(self.SB / (self.SB + self.CS), 3)
        if self.swings > 0:
            self.zMissA = round(self.zMissT / self.swings, 2)
        self.slash = str(self.AVG) + '/' + str(self.OBP) + '/' + str(self.SLG)

    def smallLine(self):
        return self.name + '(' + str(self.vis) + ',' + str(self.con) + ',' + str(self.pow) + ';' + str(round(self.OPS, 2)) + ')'

    def canGetThere(self, dist, time):
        if self.outOfPos:
            return dist < (20 + self.speed) * (time-1.5 + (.1*self.field)) + (self.field / 2)
        else:
            return dist < (20 + self.speed) * (time-2.5 + (.1*self.field)) + (self.field / 2)

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
        self.age += 1
        self.contract -= 1
