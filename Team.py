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
        self.hitters = pandas.DataFrame(columns=['Name', 'Primary', 'Secondary', 'Overall', 'Offense', 'Fielding', 'Speed', 'Available'])
        self.rotation = pandas.DataFrame(columns=['Name', 'Hand', 'Arsenal', 'Overall', 'Release', 'Extension', 'Available'])
        self.bullpen = pandas.DataFrame(columns=['Name', 'Hand', 'Arsenal', 'Overall', 'Release', 'Extension', 'Available'])
        self.baselineRosters()  # Gives initial players
        self.lineupCard = Lineup(self.rotation, self.hitters, self.ABR)
        self.played = 0
        self.wins = 0
        self.pWins = 0
        self.runsFor = 0
        self.runsAgainst = 0
        self.winDivision = False

    def baselineRosters(self):
        for i in hitterPos:  # Gives at least one player who's primary position is each pos
            cur = Hitter(nameGen(), i, random.choice(hitterHand))
            if i in infieldPos:
                second = random.choice(infieldPos)  # Infielders get infield secondary positions
            else:
                second = random.choice(outfieldPos)  # Outfielders stay in the outfield
            cur.secondary = second
            self.hitters.loc[len(self.hitters)] = [cur, cur.pos, cur.secondary, cur.overall, cur.offense, cur.field, cur.speed, cur.available]
        for i in range(5):  # Round out to 13 hitters, I use a 26-man roster
            cur = Hitter(nameGen(), random.choice(hitterPos), random.choice(hitterHand))
            if i == 0:  # At least one more catcher
                cur.pos = 'C '
            if cur.pos in infieldPos:
                second = random.choice(infieldPos)
            else:
                second = random.choice(outfieldPos)
            cur.secondary = second
            self.hitters.loc[len(self.hitters)] = [cur, cur.pos, cur.secondary, cur.overall, cur.offense, cur.field, cur.speed, cur.available]
        for i in range(5):  # Starting pitchers
            cur = Pitcher(nameGen(), 'SP', random.choice(pitcherHand))
            self.rotation.loc[len(self.rotation)] = [cur, cur.hand, cur.arsenal, cur.overall, cur.release, cur.extension, cur.available]
        for i in range(8):  # Bullpen, again 13 total pitchers
            cur = Pitcher(nameGen(), 'RP', random.choice(pitcherHand))
            self.bullpen.loc[len(self.bullpen)] = [cur, cur.hand, cur.arsenal, cur.overall, cur.release, cur.extension, cur.available]
        self.hitters.sort_values(['Overall', 'Offense'], inplace=True, ascending=False)
        self.rotation.sort_values(['Overall', 'Extension'], inplace=True, ascending=False)
        self.bullpen.sort_values(['Overall', 'Extension'], inplace=True, ascending=False)
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
                cur = self.hitters[((self.hitters['Primary']==posNotation[i]) | (self.hitters['Secondary']==posNotation[i])) & ~self.hitters['Name'].isin(self.lineupCard.dAlign) & self.hitters['Available']==True].iloc[0]['Name']
                # Best available hitter with positional eligibility who hasn't already been placed in the lineup
                self.lineupCard.dAlign[i] = cur
                self.lineupCard.battingOrder.loc[len(self.lineupCard.battingOrder)] = [cur, posNotation[i], cur.offense, cur.OPS]
            except IndexError:  # No Available hitter with positional eligibility not in roster already
                pushback.append(i)
        for i in pushback:
            cur = self.hitters[~self.hitters['Name'].isin(self.lineupCard.dAlign) & self.hitters['Available']==True].iloc[0]['Name']
            cur.outOfPos = True
            self.lineupCard.dAlign[i] = cur
            self.lineupCard.battingOrder.loc[len(self.lineupCard.battingOrder)] = [cur, posNotation[i], cur.offense,
                                                                                   cur.OPS]
        self.lineupCard.battingOrder.sort_values(['Offense', 'OPS'], ascending=False, inplace=True)
        self.bullpen['Available'] = [i.available for i in list(self.bullpen['Name'])]
        self.lineupCard.bullpen = self.bullpen
        # self.lineupCard.printout()

    def __str__(self):
        return self.name


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

    def printout(self):  # Shows starting lineups
        print(self.ABR, pandas.concat([self.battingOrder, pandas.DataFrame([[self.dAlign[1], 'SP', self.dAlign[1].overall, self.dAlign[1].ERA]], columns=['Name', 'Position', 'Offense', 'OPS'])], ignore_index=True))
        # print(self.bullpen)

    def statsUP(self):
        for i in self.battingOrder['Name']:
            i.calcStats()
        for i in self.rotation['Name']:
            i.calcStats()
        for i in self.bullpen['Name']:
            i.calcStats()

    def usage(self):
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
        rester = random.choice(restDay)
        rester.available = False
        # print(self.ABR, rester.usage, rester, 'taking tomorrow off.')


class ASTeam:  # This felt like hacking my own code to make a game play with fake teams
    def __init__(self, name, ABR, defense, hitters, bullpen):
        self.name = name
        self.ABR = ABR
        self.lineupCard = ASLineup(defense, hitters, bullpen, ABR)
        self.played = 0
        self.wins = 0
        self.runsFor = 0
        self.runsAgainst = 0

    def setLineup(self):
        pass

    def __str__(self):
        return self.name


class ASLineup:
    def __init__(self, defense, hitters, bullpen, ABR):
        self.ABR = ABR
        self.dAlign = defense
        self.battingOrder = hitters
        self.bullpen = bullpen
        self.relieversUsed = []


    def printout(self):
        #pandas.DataFrame(columns=['Name', 'Position', 'Offense', 'OPS'])
        print(pandas.concat([self.battingOrder, pandas.DataFrame([[self.dAlign[1], self.dAlign[1].team, 'SP', self.dAlign[1].overall, self.dAlign[1].ERA]], columns=['Name', 'Team', 'Position', 'Offense', 'OPS'])], ignore_index=True))
        print(self.bullpen)

    def statsUP(self):
        pass

    def usage(self):  # AS teams don't give rest days
        pass
