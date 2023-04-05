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
        self.presets = []
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
        self.rAdded = 0
        self.wR = 0
        # calc Stats
        self.IP = 0
        self.ERA = 0
        self.WHIP = 0
        self.Kp = 0
        self.wRA = 0

    def __str__(self):
        return self.name

    def record(self):
        return '(' + str(self.W) + '-' + str(self.L) + ')'

    def calcStats(self):
        self.IP = round(self.OR / 3, 1)
        if self.IP > 0:
            self.ERA = round((self.ER * 9) / self.IP, 2)
            self.wRA = round((self.wR * 9) / self.IP, 2)
            self.WHIP = round((self.H + self.BB) / self.IP, 2)
        if self.BF > 0:
            self.Kp = round(self.K / self.BF, 3)

    def smallLine(self):
        return self.name + '(' + str(self.age) + ';' + str(self.cont) + ',' + str(self.velo) + ',' + str(self.move) + ';' + str(round(self.ERA, 2)) + ')'

    def idLine(self):
        return self.pos + '    ' + self.name + '(' + str(self.age) + ';' + str(self.cont) + ',' + str(self.velo) + ',' + str(self.move) + ',' + str(self.field) + ',' + str(self.speed) + ')'

    def bigLine(self):
        return f'{self.team} {self.pos}    {self.name} ({self.age};{self.cont},{self.velo},{self.move},{self.field},{self.speed}):' \
               f' {self.IP} IP, {self.record()}, {self.S} Saves, {round((self.S+self.Hold) / self.SO, 2) if self.SO > 0 else 0} S+H%, {self.ERA} ERA,' \
               f' {self.WHIP} WHIP, {self.Kp} K%, {round(self.rAdded, 2)} RA, {self.wRA} wRA'

    def canGetThere(self, dist, time):
        return dist < (17 + .5 * self.speed) * max(time - 1.1 + (.05*self.field), 0) + (1 + .5*self.field)

    def reset(self):  # Year to year reset
        self.available = True
        self.usage = 0
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
        self.rAdded = 0
        self.wR = 0
        self.IP = 0
        self.ERA = 0
        self.wRA = 0
        self.WHIP = 0
        self.Kp = 0
        self.age += 1
        self.boost(ageCurve(self.age, controlled=self.controlled))
        self.contract[0] -= 1
        self.offers = []

    def boost(self, x):
        if self.controlled:
            print('X is:', x)
        if not self.controlled:
            self.cont += x
            self.velo += x
            self.move += x
            self.field += x
            self.speed += x
        else:
            if x > 0:
                bank = x * 4
                print('You currently:', self.idLine(), self.arStr)
                print(bank)
                newP = input('Input anything to spend 2 on learning a new pitch, blank to pass')
                if newP and bank >= 2:
                    bank -= 2
                    print('you have:', self.arsenal)
                    for i in range(len(list(pitches.keys()))):
                        if list(pitches.keys())[i] not in self.arsenal:
                            print(i, list(pitches.keys())[i])
                    try:
                        pick = int(input('Input the number corresponding to the pitch you want'))
                        self.arsenal.append(list(pitches.keys())[pick])
                        self.arStr = ''
                        for i in self.arsenal:
                            self.arStr = self.arStr + i[0:2]
                    except Exception:
                        print('u did it wrong chump, take ur money back')
                        bank += 2
                    pre = True
                    while pre:
                        pre = input('Input anything to add a preset, nothing to skip')
                        if not pre:
                            break
                        print(self.arsenal)
                        try:
                            choice = int(input('Which pitch do you want to use, first is 0, second is 1, etc.'))
                            pType = self.arsenal[choice]
                        except Exception:  # If user messes up, so the entire thing doesnt come crashing down
                            print('bad input')
                            continue
                        try:
                            xPick = float(input('X-coordinate aim?'))
                            yPick = float(input('Y-coordinate aim?'))
                        except ValueError:
                            print('bad input')
                            continue
                        self.presets.append([pType, xPick, yPick])
                try:
                    control = int(input('Bank Remaining: ' + str(bank) + '. How many towards control?'))
                except ValueError:
                    print('Bad Input, set to 0')
                    control = 0
                if control > bank:
                    control = bank
                bank -= control
                try:
                    velocity = int(input('Bank Remaining: ' + str(bank) + '. How many towards velocity?'))
                except ValueError:
                    print('Bad Input, set to 0')
                    velocity = 0
                if velocity > bank:
                    velocity = bank
                bank -= velocity
                try:
                    movement = int(input('Bank Remaining: ' + str(bank) + '. How many towards movement?'))
                except ValueError:
                    print('Bad Input, set to 0')
                    movement = 0
                if movement > bank:
                    movement = bank
                bank -= movement
                try:
                    fielding = int(input('Bank Remaining: ' + str(bank) + '. How many towards fielding (2x Value)?'))
                except ValueError:
                    print('Bad Input, set to 0')
                    fielding = 0
                if fielding > bank:
                    fielding = bank
                bank -= fielding
                try:
                    speed = int(input('Bank Remaining: ' + str(bank) + '. How many towards speed (2x Value)?'))
                except ValueError:
                    print('Bad Input, set to 0')
                    speed = 0
                if speed > bank:
                    speed = bank
                bank -= speed
                self.cont += control
                self.velo += velocity
                self.move += movement
                self.field += fielding * 2
                self.speed += speed * 2
            else:
                dud = input('woobly doobly')
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
        if self.controlled:
            for i in range(len(self.offers)):
                print(i, self.offers[i][0], 'offers a contract for', self.offers[i][1], 'years', self.offers[i][2], 'AAV.')
            if len(self.offers) == 0:
                dud = input('You were not offered any contracts in this round. Hit enter to advance')
            else:
                try:
                    choice = int(input('Would u like to sign any of these (input their number or blank to stick around)'))
                    bestOffer = self.offers[choice]
                except Exception:
                    for i in self.offers:
                        if i[1] * (i[2] ** 2) > bestValue:
                            bestValue = i[1] * (i[2] ** 2)
                            bestOffer = i
        else:
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
        self.rAdded = 0
        self.wR = 0
        # CalcStats
        self.AVG = 0
        self.OBP = 0
        self.SLG = 0
        self.OPS = 0
        self.Sp = 0
        self.zMissA = 0
        self.slash = ''
        self.BABIP = 0
        self.wRCp = 0

    def __str__(self):
        return self.name

    def calcStats(self):
        if self.PA > 0:
            self.OBP = round((self.H + self.BB) / self.PA, 3)
            self.wRCp = round(100 * ((self.wR / self.PA) / leaguewideRC), 1)
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
        return self.name + '(' + str(self.age) + ';' + str(self.con) + ',' + str(self.pow) + ',' + str(self.vis) + ';' + str(round(self.OPS, 2)) + ')'

    def idLine(self):
        return self.pos + '/' + self.secondary + ' ' + self.name + '(' + str(self.age) + ';' + str(self.con) + ',' + \
               str(self.pow) + ',' + str(self.vis) + ',' + str(self.field) + ',' + str(self.speed) + ')'

    def bigLine(self):
        return f'{self.team} {self.pos}/{self.secondary} {self.name} ({self.age};{self.con},{self.pow},{self.vis},{self.field},{self.speed}):' \
               f' {self.PA} PA, {self.slash}, {self.HR} HR, {self.SB}/{self.SB+self.CS} SB, {self.RBI} RBI, {round(self.rAdded, 2)} RA, {self.wRCp} wRC+'

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
        self.rAdded = 0
        self.wR = 0
        self.AVG = 0
        self.OBP = 0
        self.SLG = 0
        self.OPS = 0
        self.wRCp = 0
        self.Sp = 0
        self.zMissA = 0
        self.slash = ''
        self.usage = 0
        self.available = True
        self.age += 1
        self.boost(ageCurve(self.age, controlled=self.controlled))
        self.contract[0] -= 1
        self.offers = []

    def boost(self, x):
        if not self.controlled:
            self.con += x
            self.pow += x
            self.vis += x
            self.field += x
            self.speed += x
        else:
            if x > 0:
                bank = x * 5
                print('You currently:', self.idLine())
                try:
                    contact = int(input('Bank Remaining: ' + str(bank) + '. How many towards contact?'))
                except ValueError:
                    print('Bad Input, set to 0')
                    contact = 0
                if contact > bank:
                    contact = bank
                bank -= contact
                try:
                    power = int(input('Bank Remaining: ' + str(bank) + '. How many towards power?'))
                except ValueError:
                    print('Bad Input, set to 0')
                    power = 0
                if power > bank:
                    power = bank
                bank -= power
                try:
                    vision = int(input('Bank Remaining: ' + str(bank) + '. How many towards vision?'))
                except ValueError:
                    print('Bad Input, set to 0')
                    vision = 0
                if vision > bank:
                    vision = bank
                bank -= vision
                try:
                    fielding = int(input('Bank Remaining: ' + str(bank) + '. How many towards fielding?'))
                except ValueError:
                    print('Bad Input, set to 0')
                    fielding = 0
                if fielding > bank:
                    fielding = bank
                bank -= fielding
                try:
                    speed = int(input('Bank Remaining: ' + str(bank) + '. How many towards speed?'))
                except ValueError:
                    print('Bad Input, set to 0')
                    speed = 0
                if speed > bank:
                    speed = bank
                bank -= speed
                self.con += contact
                self.pow += power
                self.vis += vision
                self.field += fielding
                self.speed += speed
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
        if self.controlled:
            for i in range(len(self.offers)):
                print(i, self.offers[i][0], 'offers a contract for', self.offers[i][1], 'years', self.offers[i][2], 'AAV.')
            if len(self.offers) == 0:
                dud = input('You were not offered any contracts in this round. Hit enter to advance')
            else:
                try:
                    choice = int(
                        input('Would u like to sign any of these (input their number or blank to stick around)'))
                    bestOffer = self.offers[choice]
                except Exception:
                    for i in self.offers:
                        if i[1] * (i[2] ** 2) > bestValue:
                            bestValue = i[1] * (i[2] ** 2)
                            bestOffer = i
        else:
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
