import numpy
from Players import *
from DirectoryWide import *
import pandas
import random

hitterHand = [-1, -1, -1, 1, 1]  # 60% of hitters are righties
pitcherHand = [-1, -1, -1, 1]  # 75% of pitchers are righties


class Team:
    def __init__(self, name, ABR):
        self.name = name
        self.ABR = ABR
        self.hitters = pandas.DataFrame(columns=['Name', 'Primary', 'Secondary', 'Overall', 'Offense', 'Available'])
        self.rotation = pandas.DataFrame(columns=['Name', 'Hand', 'Arsenal', 'Core', 'Extension'])
        self.bullpen = pandas.DataFrame(columns=['Name', 'Hand', 'Arsenal', 'Core', 'Extension', 'Available'])
        self.baselineRosters()  # Gives initial players
        self.lineupCard = Lineup(self.rotation, self.hitters, self.ABR)
        self.played = 0
        self.wins = 0
        self.pWins = 0
        self.runsFor = 0
        self.runsAgainst = 0
        self.winDivision = False
        self.seed = ''
        self.prevWins = 0
        self.needs = []
        self.prospects = None
        self.values = [0] * 8
        self.controlled = False
        for i in range(7):
            self.values[i] = random.randrange(1, 4)
        self.values[7] = random.randrange(1, 3)
        self.budget = round(numpy.random.normal(500, 100))
        self.streak = 0

    def setTeam(self):
        for z in self.hitters['Name']:
            z.team = self.ABR
        for z in self.rotation['Name']:
            z.team = self.ABR
        for z in self.bullpen['Name']:
            z.team = self.ABR

    def baselineRosters(self):
        for i in hitterPos:  # Gives at least one player who's primary position is each pos
            cur = Hitter(nameGen(), i, hand=random.choice(hitterHand), top=8)
            cur.boost(ageCurve(cur.age, base=True))
            if i in infieldPos:
                second = random.choice(infieldPos)  # Infielders get infield secondary positions
            else:
                second = random.choice(outfieldPos)  # Outfielders stay in the outfield
            cur.secondary = second
            self.hitters.loc[len(self.hitters)] = [cur, cur.pos, cur.secondary, cur.overall, cur.offense, cur.available]
        for i in range(5):  # Round out to 13 hitters, I use a 26-man roster
            cur = Hitter(nameGen(), random.choice(hitterPos), hand=random.choice(hitterHand), top=8)
            cur.boost(ageCurve(cur.age, base=True))
            if i == 0:  # At least one more catcher
                cur.pos = 'C '
            if cur.pos in infieldPos:
                second = random.choice(infieldPos)
            else:
                second = random.choice(outfieldPos)
            cur.secondary = second
            self.hitters.loc[len(self.hitters)] = [cur, cur.pos, cur.secondary, cur.overall, cur.offense, cur.available]
        for i in range(5):  # Starting pitchers
            cur = Pitcher(nameGen(), 'SP', hand=random.choice(pitcherHand), top=8)
            cur.boost(ageCurve(cur.age, base=True))
            self.rotation.loc[len(self.rotation)] = [cur, cur.hand, cur.arStr, cur.overall, cur.extension]
        for i in range(8):  # Bullpen, again 13 total pitchers
            cur = Pitcher(nameGen(), 'RP', hand=random.choice(pitcherHand), top=8)
            cur.boost(ageCurve(cur.age, base=True))
            self.bullpen.loc[len(self.bullpen)] = [cur, cur.hand, cur.arStr, cur.overall, cur.extension, cur.available]
        self.hitters.sort_values(['Overall', 'Offense'], inplace=True, ascending=False)
        self.rotation.sort_values(['Core', 'Extension'], inplace=True, ascending=False)
        self.bullpen.sort_values(['Core', 'Extension'], inplace=True, ascending=False)
        """
        self.hitters.set_index('Name', inplace=True)
        self.rotation.set_index('Name', inplace=True)
        """
        # self.bullpen.set_index('Name', inplace=True)

    def setLineup(self):  # Game by game
        self.hitters.sort_values(['Overall', 'Offense'], inplace=True, ascending=False)
        self.hitters['Available'] = [i.available for i in list(self.hitters['Name'])]  # Only use Available hitters
        pushback = [0]  # Do these at the end with no positional requirements and a fielding stat penalty, 0 is the DH
        self.lineupCard.reset()
        for i in list(self.hitters['Name']):
            i.outOfPos = False
        SP = self.rotation.iloc[self.lineupCard.rotMarker]['Name']
        self.lineupCard.rotMarker = (self.lineupCard.rotMarker + 1) % 5
        self.lineupCard.dAlign[1] = SP
        for i in range(2, 10):
            try:
                cur = self.hitters[
                    ((self.hitters['Primary'] == posNotation[i]) | (self.hitters['Secondary'] == posNotation[i])) & ~
                    self.hitters['Name'].isin(self.lineupCard.dAlign) & self.hitters['Available'] == True].iloc[0][
                    'Name']
                # Best available hitter with positional eligibility who hasn't already been placed in the lineup
                self.lineupCard.dAlign[i] = cur
                self.lineupCard.battingOrder.loc[len(self.lineupCard.battingOrder)] = [cur, posNotation[i], cur.offense,
                                                                                       cur.OPS]
            except IndexError:  # No Available hitter with positional eligibility not in roster already
                pushback.append(i)
        for i in pushback:
            cur = self.hitters[~self.hitters['Name'].isin(self.lineupCard.dAlign) & self.hitters['Available'] == True].iloc[0]['Name']
            cur.outOfPos = True
            self.lineupCard.dAlign[i] = cur
            self.lineupCard.battingOrder.loc[len(self.lineupCard.battingOrder)] = [cur, posNotation[i], cur.offense,
                                                                                   cur.OPS]
        self.lineupCard.battingOrder.sort_values(['Offense', 'OPS'], ascending=False, inplace=True)
        self.bullpen['Available'] = [i.available for i in list(self.bullpen['Name'])]
        self.lineupCard.bullpen = self.bullpen
        for i in self.lineupCard.bullpen['Name']:
            i.saveOp = False
        self.lineupCard.dAlign[1].saveOp = False
        # self.lineupCard.printout()

    def __str__(self):
        return self.name

    def record(self):
        return '(' + str(self.wins) + '-' + str(self.played - self.wins) + ')'

    def reset(self):
        FAs = pandas.DataFrame(columns=['Name', 'Pos1', 'Pos2', 'Age', 'Core', 'OVR', 'Value'])
        for i in self.hitters['Name']:
            i.reset()
            if i.contract[0] <= 0:
                i.team = None
                FAs.loc[len(FAs)] = [i, i.pos, i.secondary, i.age, i.offense, i.overall, 0]
                self.hitters.drop(self.hitters[self.hitters['Name'] == i].index, inplace=True)
        for i in self.rotation['Name']:
            i.reset()
            if i.contract[0] <= 0:
                i.team = None
                FAs.loc[len(FAs)] = [i, i.pos, numpy.NaN, i.age, i.overall, i.total, 0]
                self.rotation.drop(self.rotation[self.rotation['Name'] == i].index, inplace=True)
        for i in self.bullpen['Name']:
            i.reset()
            if i.contract[0] <= 0:
                i.team = None
                FAs.loc[len(FAs)] = [i, i.pos, numpy.NaN, i.age, i.overall, i.total, 0]
                self.bullpen.drop(self.bullpen[self.bullpen['Name'] == i].index, inplace=True)
        self.hitters.reset_index(drop=True, inplace=True)
        self.rotation.reset_index(drop=True, inplace=True)
        self.bullpen.reset_index(drop=True, inplace=True)
        self.played = 0
        self.prevWins = self.wins
        self.wins = 0
        self.pWins = 0
        self.runsFor = 0
        self.runsAgainst = 0
        self.winDivision = False
        self.seed = ''
        self.streak = 0
        return FAs

    def softReset(self):
        self.played = 0
        self.wins = 0
        self.runsFor = 0
        self.runsAgainst = 0

    def needCheck(self):  # [Needed Hitters, By position, Needed pitchers, [SP, RP]]
        needs = [0, [None, None, 0, 0, 0, 0, 0, 0, 0, 0], 0, 0]
        needs[0] = 13 - len(self.hitters)
        for i in range(2, 10):
            needs[1][i] = clamp(2 - len(self.hitters[(
                        (self.hitters['Primary'] == posNotation[i]) | (self.hitters['Secondary'] == posNotation[i]))]),
                                0, 13)
        needs[2] = 5 - len(self.rotation)
        needs[3] = 8 - len(self.bullpen)
        self.needs = needs

    def prospectsAvailable(self):
        self.prospects = pandas.DataFrame(columns=['Name', 'Pos1', 'Pos2', 'Age', 'Core', 'OVR', 'Value'])
        inf = Hitter(nameGen(), random.choice(infieldPos), hand=random.choice(hitterHand), top=8)
        inf.age = 1
        inf.secondary = random.choice(infieldPos)
        self.prospects.loc[0] = [inf, inf.pos, inf.secondary, 1, inf.offense, inf.overall, 0]
        out = Hitter(nameGen(), random.choice(outfieldPos), hand=random.choice(hitterHand), top=8)
        out.age = 1
        out.secondary = random.choice(outfieldPos)
        self.prospects.loc[1] = [out, out.pos, out.secondary, 1, out.offense, out.overall, 0]
        sp = Pitcher(nameGen(), 'SP', hand=random.choice(pitcherHand), top=8)
        sp.age = 1
        self.prospects.loc[2] = [sp, 'SP', numpy.nan, 1, sp.overall, sp.total, 0]
        rp = Pitcher(nameGen(), 'RP', hand=random.choice(pitcherHand), top=8)
        rp.age = 1
        self.prospects.loc[3] = [rp, 'RP', numpy.nan, 1, rp.overall, rp.total, 0]

    def contractBundle(self, fa, roundNum, year, p):
        if year == 1:
            remBudget = self.budget / 2
        elif year == 2:
            remBudget = self.budget * .75
        else:
            remBudget = self.budget
        for i in self.hitters['Name']:
            remBudget -= i.contract[1]
        for i in self.rotation['Name']:
            remBudget -= i.contract[1]
        for i in self.bullpen['Name']:
            remBudget -= i.contract[1]
        remBudget = round(remBudget, 1)
        if p > 1:
            print(remBudget)
        if (self.needs[0] + self.needs[2] + self.needs[3]) * 2 > remBudget:
            if p:
                print('Out of Cash')
            for i in range(self.needs[0]):
                dum = Hitter(nameGen(), '1B', hand=1, top=1)
                (dum.age, dum.secondary, dum.value, dum.cost) = (0, '1B', 0, 2)
                self.hitters.loc[len(self.hitters)] = numpy.array([dum, dum.pos, dum.secondary, dum.overall,
                                                                   dum.offense, dum.available], dtype=object)
            for i in range(self.needs[2]):
                dum = Pitcher(nameGen(), 'SP', hand=1, top=1)
                (dum.age, dum.value, dum.cost) = (0, 0, 2)
                self.rotation.loc[len(self.rotation)] = numpy.array([dum, dum.hand, dum.arStr, dum.overall,
                                                                     dum.extension], dtype=object)
            for i in range(self.needs[3]):
                dum = Pitcher(nameGen(), 'SP', hand=1, top=1)
                (dum.age, dum.value, dum.cost) = (0, 0, 2)
                self.bullpen.loc[len(self.bullpen)] = numpy.array([dum, dum.hand, dum.arStr, dum.overall,
                                                                   dum.extension, dum.available], dtype=object)
        avHitters = pandas.concat([fa[~fa['Pos2'].isnull()], self.prospects[~self.prospects['Pos2'].isnull()]], ignore_index=True)
        for i in avHitters['Name']:
            i.value = self.setValue(i, roundNum)
            i.cost = i.value if i.age > 1 else 2
        avHitters['Value'] = [i.value for i in avHitters['Name']]
        avHitters['Cost'] = [i.cost for i in avHitters['Name']]
        avSPs = pandas.concat([fa[fa['Pos1'] == 'SP'], self.prospects[self.prospects['Pos1'] == 'SP']], ignore_index=True)
        for i in avSPs['Name']:
            i.value = self.setValue(i, roundNum)
            i.cost = i.value if i.age > 1 else 2
        avSPs['Value'] = [i.value for i in avSPs['Name']]
        avSPs['Cost'] = [i.cost for i in avSPs['Name']]
        avRPs = pandas.concat([fa[fa['Pos1'] == 'RP'], self.prospects[self.prospects['Pos1'] == 'RP']], ignore_index=True)
        for i in avRPs['Name']:
            i.value = self.setValue(i, roundNum)
            i.cost = i.value if i.age > 1 else 2
        avRPs['Value'] = [i.value for i in avRPs['Name']]
        avRPs['Cost'] = [i.cost for i in avRPs['Name']]
        avHitters.sort_values(['Value', 'OVR'], inplace=True, ascending=False)
        avSPs.sort_values(['Value', 'OVR'], inplace=True, ascending=False)
        avRPs.sort_values(['Value', 'OVR'], inplace=True, ascending=False)
        if self.controlled:
            self.selfContracts(remBudget, avHitters, avSPs, avRPs, roundNum)
        else:
            self.buildBundles(remBudget, avHitters, avSPs, avRPs, roundNum, p)

    def selfContracts(self, remBudget, avHitters, avSPs, avRPs, roundNum):
        print(*self.needs)
        avHitters['Contact'] = [i.con for i in avHitters['Name']]
        avHitters['Power'] = [i.pow for i in avHitters['Name']]
        avHitters['Vision'] = [i.vis for i in avHitters['Name']]
        avHitters['Fielding'] = [i.field for i in avHitters['Name']]
        avHitters['Speed'] = [i.speed for i in avHitters['Name']]
        avSPs['Control'] = [i.cont for i in avSPs['Name']]
        avSPs['Velocity'] = [i.velo for i in avSPs['Name']]
        avSPs['Movement'] = [i.move for i in avSPs['Name']]
        avSPs['Fielding'] = [i.field for i in avSPs['Name']]
        avSPs['Speed'] = [i.speed for i in avSPs['Name']]
        avSPs['Arsenal'] = [i.arStr for i in avSPs['Name']]
        avRPs['Control'] = [i.cont for i in avRPs['Name']]
        avRPs['Velocity'] = [i.velo for i in avRPs['Name']]
        avRPs['Movement'] = [i.move for i in avRPs['Name']]
        avRPs['Fielding'] = [i.field for i in avRPs['Name']]
        avRPs['Speed'] = [i.speed for i in avRPs['Name']]
        avRPs['Arsenal'] = [i.arStr for i in avRPs['Name']]
        # your players
        hitters = self.hitters.copy()
        rotation = self.rotation.copy()
        bullpen = self.bullpen.copy()
        hitters['Contact'] = [i.con for i in hitters['Name']]
        hitters['Power'] = [i.pow for i in hitters['Name']]
        hitters['Vision'] = [i.vis for i in hitters['Name']]
        hitters['Fielding'] = [i.field for i in hitters['Name']]
        hitters['Speed'] = [i.speed for i in hitters['Name']]
        hitters['Age'] = [i.age for i in hitters['Name']]
        hitters['Duration'] = [i.contract[0] for i in hitters['Name']]
        hitters['Salary'] = [i.contract[1] for i in hitters['Name']]
        rotation['Control'] = [i.cont for i in rotation['Name']]
        rotation['Velocity'] = [i.velo for i in rotation['Name']]
        rotation['Movement'] = [i.move for i in rotation['Name']]
        rotation['Fielding'] = [i.field for i in rotation['Name']]
        rotation['Speed'] = [i.speed for i in rotation['Name']]
        rotation['Age'] = [i.age for i in rotation['Name']]
        rotation['Duration'] = [i.contract[0] for i in rotation['Name']]
        rotation['Salary'] = [i.contract[1] for i in rotation['Name']]
        bullpen['Control'] = [i.cont for i in bullpen['Name']]
        bullpen['Velocity'] = [i.velo for i in bullpen['Name']]
        bullpen['Movement'] = [i.move for i in bullpen['Name']]
        bullpen['Fielding'] = [i.field for i in bullpen['Name']]
        bullpen['Speed'] = [i.speed for i in bullpen['Name']]
        bullpen['Age'] = [i.age for i in bullpen['Name']]
        bullpen['Duration'] = [i.contract[0] for i in bullpen['Name']]
        bullpen['Salary'] = [i.contract[1] for i in bullpen['Name']]
        with pandas.ExcelWriter('UserFAs.xlsx') as writer:
            avHitters.to_excel(writer, sheet_name='FA Hitters')
            avSPs.to_excel(writer, sheet_name='FA Starters')
            avRPs.to_excel(writer, sheet_name='FA Relievers')
            hitters.to_excel(writer, sheet_name='Your Hitters')
            rotation.to_excel(writer, sheet_name='Your Starters')
            bullpen.to_excel(writer, sheet_name='Your Relievers')
        going = True
        toGo = self.needs.copy()
        while going:
            print('Remaining Budget:', remBudget)
            going = input('Input anything to make an offer, blank to stop for the round')
            if not going:
                break
            try:
                group = int(input('1 for hitter, 2 for SP, 3 for RP'))
                if group == 1:
                    toGo[0] -= 1
                    if toGo[0] < 0:
                        print('Already 13 hitters on roster/offered contract.')
                        raise ValueError
                    loc = int(input('Input the key of hitter you wish to offer a contract'))
                    player = avHitters.loc[loc].Name
                    if player.age == 1:
                        print('Prospect. 3yr 2AAV offer.')
                        salary = 2
                        duration = 3
                    else:
                        salary = int(input('AAV offer?'))
                        duration = int(input('How many years is the contract'))
                elif group == 2:
                    toGo[2] -= 1
                    if toGo[2] < 0:
                        print('Already 5 SPs on roster/offered contract.')
                        raise ValueError
                    loc = int(input('Input the key of starter you wish to offer a contract'))
                    player = avSPs.loc[loc].Name
                    if player.age == 1:
                        print('Prospect. 3yr 2AAV offer.')
                        salary = 2
                        duration = 3
                    else:
                        salary = int(input('AAV offer?'))
                        duration = int(input('How many years is the contract'))
                elif group == 3:
                    toGo[3] -= 1
                    if toGo[3] < 0:
                        print('Already 8 RPs on roster/offered contract.')
                        raise ValueError
                    loc = int(input('Input the key of reliever you wish to offer a contract'))
                    player = avRPs.loc[loc].Name
                    if player.age == 1:
                        print('Prospect. 3yr 2AAV offer.')
                        salary = 2
                        duration = 3
                    else:
                        salary = int(input('AAV offer?'))
                        duration = int(input('How many years is the contract'))
                else:
                    raise ValueError
                if salary > remBudget:
                    print('Too expensive')
                    raise ValueError
                player.offers.append([self, duration, salary])
                if isinstance(player, Hitter):
                    print(self.name, 'offer a', duration, 'year,', salary, 'AAV contract to', player.pos + '/'
                          + player.secondary, player.smallLine())
                else:
                    print(self.name, 'offer a', duration, 'year,', salary, 'AAV contract to', player.pos, player.smallLine())
                remBudget -= salary
            except ValueError:
                print('Bad input')
                continue
        dud = input('CLOSE THE EXCEL FILE OR ELSE IT WONT UPDATE, THEN HIT ENTER')



    def buildBundles(self, remBudget, avHitters, avSPs, avRPs, roundNum, p):
        if roundNum > 15:
            print(avRPs)
        # print(avHitters.head())
        # print(avSPs.head())
        # print(avRPs.head())
        hBundles = [None] * 35
        for j in range(35):
            go = True
            tries = 1
            while go and tries < 250:
                val = 0
                cost = 0
                halfCost = 0
                try:
                    cur = random.sample(list(avHitters['Name']), self.needs[0])
                    toGo = self.needs[1].copy()
                    for i in cur:
                        toGo[posNotation.index(i.pos)] -= 1
                        toGo[posNotation.index(i.secondary)] -= 1
                        val += i.value
                        cost += i.cost
                        halfCost += max(round(i.cost / 2, 1), 2)
                    go = False
                    for i in toGo[2:]:
                        if i > 0:
                            go = True
                    tries += 1
                except ValueError:
                    print(avHitters)
                    cur = list(avHitters['Name'])
                    while len(cur) < self.needs[0]:
                        dum = Hitter(nameGen(), '1B', hand=1, top=1)
                        (dum.age, dum.secondary, dum.value, dum.cost) = (0, '1B', 0, 2)
                        cur = cur + [dum]
                    for i in cur:
                        val += i.value
                        cost += i.cost
                        halfCost += max(round(i.cost / 2, 1), 2)
            if tries > 250 and roundNum > 2:
                val = 0
                cost = 0
                halfCost = 0
                try:
                    cur = random.sample(list(avHitters['Name']), self.needs[0])
                    for i in cur:
                        val += i.value
                        cost += i.cost
                        halfCost += max(round(i.cost / 2, 1), 2)
                except ValueError:
                    cur = list(avHitters['Name'])
                    while len(cur) < self.needs[0]:
                        dum = Hitter(nameGen(), '1B', hand=1, top=1)
                        (dum.age, dum.secondary, dum.value, dum.cost) = (0, '1B', 0, 2)
                        self.prospects.loc[len(self.prospects)] = [dum, dum.pos, dum.secondary, 1, dum.offense,
                                                                   dum.overall, 0]
                        cur = cur + [dum]
                    for i in cur:
                        val += i.value
                        cost += i.cost
                        halfCost += max(round(i.cost / 2, 1), 2)
            elif tries > 250:
                cur = ([None] * self.needs[0]) + [0, math.inf, math.inf]
            hBundles[j] = cur + [val, cost, halfCost]
        spBundles = [None] * 25
        for j in range(25):
            val = 0
            cost = 0
            halfCost = 0
            try:
                cur = random.sample(list(avSPs['Name']), self.needs[2])
                for i in cur:
                    val += i.value
                    cost += i.cost
                    halfCost += max(round(i.cost / 2, 1), 2)
            except ValueError:
                print(avSPs)
                cur = list(avSPs['Name'])
                while len(cur) < self.needs[2]:
                    dum = Pitcher(nameGen(), 'SP', hand=1, top=1)
                    (dum.age, dum.value, dum.cost) = (0, 0, 2)
                    self.prospects.loc[len(self.prospects)] = [dum, 'SP', numpy.nan, 1, dum.overall, dum.total, 0]
                    cur = cur + [dum]
                for i in cur:
                    val += i.value
                    cost += i.cost
                    halfCost += max(round(i.cost / 2, 1), 2)
            spBundles[j] = cur + [val, cost, halfCost]
        rpBundles = [None] * 30
        for j in range(30):
            val = 0
            cost = 0
            halfCost = 0
            try:
                cur = random.sample(list(avRPs['Name']), self.needs[3])
                for i in cur:
                    val += i.value
                    cost += i.cost
                    halfCost += max(round(i.cost / 2, 1), 2)
            except ValueError:
                print(avRPs)
                cur = list(avRPs['Name'])
                while len(cur) < self.needs[3]:
                    dum = Pitcher(nameGen(), 'RP', hand=1, top=1)
                    (dum.age, dum.value, dum.cost) = (0, 0, 2)
                    cur = cur + [dum]
                    print(cur, 'after dummy added')
                for i in cur:
                    val += i.value
                    cost += i.cost
                    halfCost += max(round(i.cost / 2, 1), 2)
            rpBundles[j] = cur + [val, cost, halfCost]
        self.buildOffers(remBudget, hBundles, spBundles, rpBundles, p)

    def buildOffers(self, remBudget, hBundles, spBundles, rpBundles, p):
        offers = []
        halfOffers = []
        bestValue = 0
        halfValue = 0
        for i in hBundles:
            for j in spBundles:
                for k in rpBundles:
                    if i[-2] + j[-2] + k[-2] <= remBudget:
                        val = i[-3] + j[-3] + k[-3]
                        if val > bestValue:
                            bestValue = val
                            offers = i[:-3] + j[:-3] + k[:-3]
                    if i[-1] + j[-1] + k[-1] <= remBudget:
                        val = i[-3] + j[-3] + k[-3]
                        if val > halfValue:
                            halfValue = val
                            halfOffers = i[:-3] + j[:-3] + k[:-3]
        self.sendOffers(offers, halfOffers, p)

    def sendOffers(self, offers, halfOffers, p):
        for i in offers:
            conLen = 3 if i.age == 1 else random.randrange(1, 5)
            i.offers.append([self, conLen, i.cost])
            if isinstance(i, Hitter) and p > 1:
                print(self.name, 'offer a', conLen, 'year,', i.cost, 'AAV contract to', i.pos + '/' + i.secondary,
                      i.smallLine())
            elif p > 1:
                print(self.name, 'offer a', conLen, 'year,', i.cost, 'AAV contract to', i.pos, i.smallLine())
        if len(offers) == 0 and len(halfOffers) > 0:
            if p > 1:
                print('Half offers')
            for i in halfOffers:
                conLen = 3 if i.age == 1 else random.randrange(1, 5)
                halfCostCur = max(round(i.cost / 2, 1), 2)
                i.offers.append([self, conLen, halfCostCur])
                if isinstance(i, Hitter) and p > 1:
                    print(self.name, 'offer a', conLen, 'year,', halfCostCur, 'AAV contract to',
                          i.pos + '/' + i.secondary,
                          i.smallLine())
                elif p > 1:
                    print(self.name, 'offer a', conLen, 'year,', halfCostCur, 'AAV contract to', i.pos, i.smallLine())

    def setValue(self, player, roundNum):
        if isinstance(player, Hitter):
            return max(
                round(((self.values[0] * player.con) + (self.values[1] * player.pow) + (self.values[2] * player.vis) +
                       (self.values[3] * .5 * (player.field + player.speed))) * (.9 ** roundNum), 1), 2)
        elif isinstance(player, Pitcher):
            return max(round(
                ((self.values[4] * player.cont) + (self.values[5] * player.velo) + (self.values[6] * player.move) +
                 (self.values[7] * .5 * (player.field + player.speed))) * (.9 ** roundNum), 1), 2)
        else:
            print('no')

    def usageReset(self):
        for i in self.hitters['Name']:
            i.available = True
            i.usage = 0
        for i in self.bullpen['Name']:
            i.available = True
            i.usage = 0
        self.lineupCard.rotMarker = 0


class Lineup:  # Lineup card, gets called within the game
    def __init__(self, rotation, hitters, ABR):
        self.ABR = ABR
        self.rotation = rotation
        self.hitters = hitters
        self.dAlign = [None] * 10  # [DH, P, C, 1B, 2B, 3B, SS, LF, CF, RF]
        self.battingOrder = pandas.DataFrame(columns=['Name', 'Position', 'Offense', 'OPS'])
        self.bullpen = None
        self.rotMarker = 0
        self.relieversUsed = []

    def reset(self):  # Before games
        self.dAlign = [None] * 10
        self.battingOrder = pandas.DataFrame(columns=['Name', 'Position', 'Offense', 'OPS'])
        self.bullpen = None
        self.relieversUsed = []

    def containsControlled(self):
        answer = None
        for i in self.dAlign:
            if i.controlled:
                answer = i
        for i in self.bullpen[self.bullpen['Available'] == True].Name:
            if i.controlled:
                answer = i
        if self.rotation.iloc[(self.rotMarker + 1) % 5]['Name'].controlled:
            answer = self.rotation.iloc[(self.rotMarker + 1) % 5]['Name']
        return answer

    def printout(self):  # Shows starting lineups
        print(pandas.concat([self.battingOrder, pandas.DataFrame(
            [[self.dAlign[1], 'SP', self.dAlign[1].overall, self.dAlign[1].ERA]],
            columns=['Name', 'Position', 'Offense', 'OPS'])], ignore_index=True))
        # print(self.bullpen)

    def statsUP(self):
        for i in self.battingOrder['Name']:
            i.calcStats()
        for i in self.rotation['Name']:
            i.calcStats()
        for i in self.bullpen['Name']:
            i.calcStats()

    def usage(self, playoff=False):
        for i in self.bullpen['Name']:
            i.available = True
            if i in self.relieversUsed:
                i.usage += 1  # Days in a row used
            else:
                i.usage = 0
            if i.usage >= 2:  # Relievers can't pitch 3 in a row
                i.available = False
        restDay = []  # One hitter from game has to rest the next one, weighted based on consecutive games played
        for i in self.hitters['Name']:
            i.available = True
            if i in list(self.battingOrder['Name']):
                i.usage += 1
            else:
                i.usage = 0
            for j in range(i.usage):
                restDay.append(i)
        size = 1 if playoff else 2
        resters = random.sample(restDay, k=size)
        for i in resters:
            i.available = False
        # print(self.ABR, rester.usage, rester, 'taking tomorrow off.')


class ASTeam:  # This felt like hacking my own code to make a game play with fake teams
    def __init__(self, name, ABR, defense, hitters, bullpen):
        self.name = name
        self.ABR = ABR
        self.defense = defense
        self.bullpen = bullpen
        self.lineupCard = ASLineup(defense, hitters, bullpen, ABR)
        self.played = 0
        self.wins = 0
        self.runsFor = 0
        self.runsAgainst = 0
        self.streak = 0
        self.controlled = False

    def record(self):
        return '(' + str(self.wins) + '-' + str(self.played - self.wins) + ')'

    def setLineup(self):
        pass

    def setTeam(self):
        for z in self.defense:
            z.team = self.ABR
        for z in self.bullpen['Name']:
            z.team = self.ABR

    def __str__(self):
        return self.name


class ASLineup:
    def __init__(self, defense, hitters, bullpen, ABR):
        self.ABR = ABR
        self.dAlign = defense
        self.battingOrder = hitters
        self.bullpen = bullpen
        self.relieversUsed = []
        self.starters = None

    def printout(self):
        print(self.starters)
        print(self.bullpen)

    def statsUP(self):
        pass

    def usage(self, playoff=False):  # AS teams don't give rest days
        pass

    def containsControlled(self):
        answer = None
        for i in self.dAlign:
            if i.controlled:
                answer = i
        return answer
