import pandas
from Gameplay import *
from Team import *
from DirectoryWide import *
import numpy
from alive_progress import alive_bar, alive_it
#"""
schedLength = input('How many games per season would you like? (20, 52, 162, Alt)')  # 1 and '' is 52, 2 is 162
if schedLength == '':
    schedLength = '52'
if schedLength == 'Alt':
    playoffSize = 'it literally doesnt matter'
else:
    playoffSize = input('What playoff format would you like? (8, 10, 12, DE)')  # 0 is 8, 1 is 10, 2 and '' is 12 (also 'DE12' for the fun one I'm gonna make)
#schedLength = '162'
#playoffSize = 'DE'

seriesHome = [None, [0], [0, 0, 0], [0, 0, 1, 1, 0], [0, 0, 1, 1, 1, 0, 0]]
# First index is series length (in wins needed), second index: 0 means better seed hosts game, 1 means worse seed

print('Building the teams...')
NLEt = [Team('Washington Nationals ', 'WSN'), Team('New York Mets        ', 'NYM'),
        Team('Atlanta Braves       ', 'ATL'), Team('Miami Marlins        ', 'MIA'),
        Team('Philadelphia Phillies', 'PHI')]  # Teams
NLCt = [Team('Chicago Cubs         ', 'CHC'), Team('Cincinnati Reds      ', 'CIN'),
        Team('St. Louis Cardinals  ', 'STL'), Team('Pittsburgh Pirates   ', 'PIT'),
        Team('Milwaukee Brewers    ', 'MIL')]
NLWt = [Team('Los Angeles Dodgers  ', 'LAD'), Team('Arizona Diamondbacks ', 'ARI'),
        Team('San Fransisco Giants ', 'SFG'), Team('San Diego Padres     ', 'SDP'),
        Team('Colorado Rockies     ', 'COL')]
ALEt = [Team('New York Yankees     ', 'NYY'), Team('Tampa Bay Rays       ', 'TBR'),
        Team('Boston Red Sox       ', 'BOS'), Team('Toronto Blue Jays    ', 'TOR'),
        Team('Baltimore Orioles    ', 'BAL')]
ALCt = [Team('Minnesota Twins      ', 'MIN'), Team('Cleveland Guardians  ', 'CLE'),
        Team('Chicago White Sox    ', 'CHW'), Team('Kansas City Royals   ', 'KCR'),
        Team('Detroit Tigers       ', 'DET')]
ALWt = [Team('Houston Astros       ', 'HOU'), Team('Oakland Athletics    ', 'OAK'),
        Team('LA Angels of Anaheim ', 'LAA'), Team('Texas Rangers        ', 'TEX'),
        Team('Seattle Mariners     ', 'SEA')]
NLEs = pandas.DataFrame(numpy.array(NLEt), columns=['Team'])  # Standings
NLCs = pandas.DataFrame(numpy.array(NLCt), columns=['Team'])
NLWs = pandas.DataFrame(numpy.array(NLWt), columns=['Team'])
ALEs = pandas.DataFrame(numpy.array(ALEt), columns=['Team'])
ALCs = pandas.DataFrame(numpy.array(ALCt), columns=['Team'])
ALWs = pandas.DataFrame(numpy.array(ALWt), columns=['Team'])
Divisions = [NLEt, NLCt, NLWt, ALEt, ALCt, ALWt]
Standings = [NLEs, NLCs, NLWs, ALEs, ALCs, ALWs]
NLt = NLEt+NLCt+NLWt
ALt = ALEt+ALCt+ALWt
NLs = pandas.concat([NLEs, NLCs, NLWs])
ALs = pandas.concat([ALEs, ALCs, ALWs])
Leagues = [NLt, ALt]
MLBt = NLt + ALt
# INTER LEAGUE
geoRivals = [(NLEt[0], ALEt[4]), (NLEt[1], ALEt[0]), (NLEt[2], ALEt[3]), (NLEt[3], ALEt[1]), (NLEt[4], ALEt[2]),
             (NLCt[0], ALCt[2]), (NLCt[1], ALCt[1]), (NLCt[2], ALCt[3]), (NLCt[3], ALCt[4]), (NLCt[4], ALCt[0]),
             (NLWt[0], ALWt[2]), (NLWt[1], ALWt[3]), (NLWt[2], ALWt[1]), (NLWt[3], ALWt[4]), (NLWt[4], ALWt[0])]
# ^ These are the real geographic rivals
geoRivals2 = [(j[1], j[0]) for j in geoRivals]  # Home/Away Flip
interleagueSlates = [None]*14
NLHomes = random.sample(list(range(14)), k=7)
for i in range(14):
    interleagueSlates[i] = [(geoRivals[0][0], geoRivals[(i + 1) % 15][1]),
                            (geoRivals[1][0], geoRivals[(i + 2) % 15][1]),
                            (geoRivals[2][0], geoRivals[(i + 3) % 15][1]),
                            (geoRivals[3][0], geoRivals[(i + 4) % 15][1]),
                            (geoRivals[4][0], geoRivals[(i + 5) % 15][1]),
                            (geoRivals[5][0], geoRivals[(i + 6) % 15][1]),
                            (geoRivals[6][0], geoRivals[(i + 7) % 15][1]),
                            (geoRivals[7][0], geoRivals[(i + 8) % 15][1]),
                            (geoRivals[8][0], geoRivals[(i + 9) % 15][1]),
                            (geoRivals[9][0], geoRivals[(i + 10) % 15][1]),
                            (geoRivals[10][0], geoRivals[(i + 11) % 15][1]),
                            (geoRivals[11][0], geoRivals[(i + 12) % 15][1]),
                            (geoRivals[12][0], geoRivals[(i + 13) % 15][1]),
                            (geoRivals[13][0], geoRivals[(i + 14) % 15][1]),
                            (geoRivals[14][0], geoRivals[i % 15][1])]
    if i not in NLHomes:
        interleagueSlates[i] = [(j[1], j[0]) for j in interleagueSlates[i]]  # Flip home and away for half the slates
geoRivalsFinal = [geoRivals]  # Later we will be adding Lists of slates, so even though it's just 1 slate still need it.
geoRivals2Final = [geoRivals2]


def roundRobin(groups):
    for q in range(1):  # This is a slightly edited of a round robin algorithm i found online and stole
        schedule = []
        for div in groups:
            w = div.copy()
            random.shuffle(w)
            if len(w) % 2 == 1:
                w.append(None)
            n = len(w)
            d = list(range(n))
            mid = n // 2
            for i in range(n - 1):
                l1 = d[:mid]
                l2 = d[mid:]
                l2.reverse()
                round = []
                for j in range(mid):
                    t1 = w[l1[j]]
                    t2 = w[l2[j]]
                    if j == 0 and i % 2 == 1:
                        round.append((t2, t1))
                    else:
                        round.append((t1, t2))
                schedule.append(round)
                # rotate list by n/2, leaving last element at the end
                d = d[mid:-1] + d[:mid] + d[-1:]
        return schedule


for i in Divisions:
    random.shuffle(i)
# DIVISIONAL
bigSched = roundRobin(Divisions)
divisionalSlates = [None]*5
for i in range(5):
    divisionalSlates[i] = bigSched[i]+bigSched[i+5]+bigSched[i+10]+bigSched[i+15]+bigSched[i+20]+bigSched[i+25]
divisionalSlates2 = [[(j[1], j[0]) for j in i] for i in divisionalSlates]

# SAME LEAGUE
biggerSched = roundRobin(Leagues)
leagueSlates = [None]*15
for i in range(15):
    leagueSlates[i] = biggerSched[i] + biggerSched[i+15]
leagueSlates2 = [[(j[1], j[0]) for j in i] for i in leagueSlates]

# 52 Game Schedule - 15 Interleague + 1 extra georival, 16 Division, 20 non-div same league
schedule52 = geoRivalsFinal + geoRivals2Final + interleagueSlates + divisionalSlates + divisionalSlates2 + leagueSlates + leagueSlates2
random.shuffle(schedule52)

# 162 Game Schedule - 52 from there^ + 2 bonus division games, all played as 3 game series
miniSlates = [[(k[0], k[1]) for k in Divisions] + [(k[2], k[3]) for k in Divisions],
              [(k[1], k[2]) for k in Divisions] + [(k[3], k[4]) for k in Divisions],
              [(k[4], k[0]) for k in Divisions]]

base = schedule52 + miniSlates
random.shuffle(base)
schedule162 = [None]*177
for i in range(177):
    schedule162[i] = base[i//3]

# 20 Game Schedule - 2 Geo Rival + 8 divisional + 10 non divisional same league, Home = Away not promised
schedule20 = geoRivalsFinal + geoRivals2Final + divisionalSlates + leagueSlates
random.shuffle(schedule20)

schedule0 = []
#"""


def series(top, bot, l, pri=1, losers=False, wins=False):  # Top seed, bottom seed, games needed to win, print value
    top.usageReset()
    bot.usageReset()
    if wins:
        if bot.wins > top.wins:  # We are going to flip em
            hold = bot
            bot = top
            top = hold
    print(top.seed, top, top.record(), 'vs.', bot.seed, bot, bot.record(), 'best of', (l*2) - 1)
    top.pWins = 0
    bot.pWins = 0
    gameNum = 0
    while top.pWins < l and bot.pWins < l:
        if seriesHome[l][gameNum] == 0:
            game(top, bot, playoff=True, p=pri)
        else:
            game(bot, top, playoff=True, p=pri)
        print(top.ABR, top.pWins, bot.pWins, bot.ABR)
        gameNum += 1
    if not losers:
        if top.pWins == l:
            return top
        elif bot.pWins == l:
            return bot
    else:
        if top.pWins == l:
            return [top, bot]
        elif bot.pWins == l:
            return [bot, top]


def playIt(schedule):  # Plays the regular season
    for i in range(len(schedule)):
        if i == (len(schedule)//6)*3:
            print('HALFWAY STANDINGS')
            for k in Standings:
                k['Played'] = [j.played for j in k['Team']]
                k['Wins'] = [j.wins for j in k['Team']]
                k['Losses'] = k['Played'] - k['Wins']
                k['WPCT'] = (1000 * k['Wins']) // k['Played']
                k['Run D'] = [(j.runsFor - j.runsAgainst) for j in k['Team']]
                k.sort_values(['WPCT', 'Run D'], inplace=True, ascending=False)  # irl tiebreak is H2H
                k.reset_index(drop=True, inplace=True)
                print(k)
            print('ALL-STAR BREAK')
            WSHost = allstarGame(int(schedLength)//2)  # Winner of the ASG gets top seed in WS
            for dkajfhdkfh in NLt+ALt:  # i got annoyed
                dkajfhdkfh.setTeam(p=False)
        print('SLATE', i+1)
        slateScores = []
        for j in schedule[i]:
            if j[0] and j[1]:
                slateScores.append(game(j[0], j[1], p=0))
        print(slateScores)
    endOfYear(int(schedLength))  # Stats Leaders
    print('DIVISION STANDINGS')
    for i in Standings:
        i['Played'] = [j.played for j in i['Team']]
        i['Wins'] = [j.wins for j in i['Team']]
        i['Losses'] = i['Played'] - i['Wins']
        i['WPCT'] = (1000 * i['Wins']) // i['Played']
        i['Run D'] = [(j.runsFor - j.runsAgainst) for j in i['Team']]
        i.sort_values(['Wins', 'Run D'], inplace=True, ascending=False)
        i.iloc[0]['Team'].winDivision = True  # Secures playoff spot
        i.reset_index(drop=True, inplace=True)
        print(i)
    print('LEAGUE STANDINGS')
    for i in [NLs, ALs]:
        i['Played'] = [j.played for j in i['Team']]
        i['Wins'] = [j.wins for j in i['Team']]
        i['Losses'] = i['Played'] - i['Wins']
        i['WPCT'] = (1000 * i['Wins']) // i['Played']
        i['Run D'] = [(j.runsFor - j.runsAgainst) for j in i['Team']]
        i['D. Winner'] = [j.winDivision for j in i['Team']]
        i.sort_values(['D. Winner', 'WPCT', 'Run D'], inplace=True, ascending=False)
        i.reset_index(drop=True, inplace=True)
    print(NLs)
    print(ALs)
    if playoffSize in ['1', '8']:
        playoffs8(NLs, ALs, WSHost)
    elif playoffSize in ['2', '10']:
        playoffs10(NLs, ALs, WSHost)
    elif playoffSize in ['DE', 'DE12']:
        playoffsDP12(NLs, ALs)
    elif playoffSize == '0':
        pass
    else:
        playoffs12(NLs, ALs, WSHost)


def playoffs12(NLs, ALs, WSHost):  # New MLB playoff format, starting 2022
    NLdw = NLs.loc[NLs['D. Winner'] == True]
    ALdw = ALs.loc[ALs['D. Winner'] == True]
    NLwc = NLs.loc[NLs['D. Winner'] == False]
    ALwc = ALs.loc[ALs['D. Winner'] == False]
    NLplay = [NLdw.iloc[0]['Team'], NLdw.iloc[1]['Team'], NLdw.iloc[2]['Team'],
           NLwc.iloc[0]['Team'], NLwc.iloc[1]['Team'], NLwc.iloc[2]['Team']]
    ALplay = [ALdw.iloc[0]['Team'], ALdw.iloc[1]['Team'], ALdw.iloc[2]['Team'],
           ALwc.iloc[0]['Team'], ALwc.iloc[1]['Team'], ALwc.iloc[2]['Team']]
    for i in NLplay:
        i.seed = 'N'+str(NLplay.index(i) + 1)
    for i in ALplay:
        i.seed = 'A'+str(ALplay.index(i) + 1)
    print('NL Playoffs')
    bracket(NLplay)  # Prints a cute lil bracket to look at
    print('AL Playoffs')
    bracket(ALplay)
    print('National League Wild Card')
    NLWC1 = series(NLplay[3], NLplay[4], 2)
    NLWC2 = series(NLplay[2], NLplay[5], 2)
    print('American League Wild Card')
    ALWC1 = series(ALplay[3], ALplay[4], 2)
    ALWC2 = series(ALplay[2], ALplay[5], 2)
    print('National League Division Series')
    NLDS1 = series(NLplay[0], NLWC1, 3)
    NLDS2 = series(NLplay[1], NLWC2, 3)
    print('American League Division Series')
    ALDS1 = series(ALplay[0], ALWC1, 3)
    ALDS2 = series(ALplay[1], ALWC2, 3)
    print('National League Championship Series')
    if NLplay.index(NLDS1) < NLplay.index(NLDS2):
        NLCS = series(NLDS1, NLDS2, 4)
    else:
        NLCS = series(NLDS2, NLDS1, 4)
    print('American League Championship Series')
    if ALplay.index(ALDS1) < ALplay.index(ALDS2):
        ALCS = series(ALDS1, ALDS2, 4)
    else:
        ALCS = series(ALDS2, ALDS1, 4)
    print('World Series')
    if WSHost == 'NL':
        WS = series(NLCS, ALCS, 4)
    else:
        WS = series(ALCS, NLCS, 4)
    print(WS, 'wins the world series!!!')


def playoffs10(NLs, ALs, WSHost):  # MLB playoff 2012-2021 except Covid 2020
    NLdw = NLs.loc[NLs['D. Winner'] == True]
    ALdw = ALs.loc[ALs['D. Winner'] == True]
    NLwc = NLs.loc[NLs['D. Winner'] == False]
    ALwc = ALs.loc[ALs['D. Winner'] == False]
    NLplay = [NLdw.iloc[0]['Team'], NLdw.iloc[1]['Team'], NLdw.iloc[2]['Team'],
           NLwc.iloc[0]['Team'], NLwc.iloc[1]['Team']]
    ALplay = [ALdw.iloc[0]['Team'], ALdw.iloc[1]['Team'], ALdw.iloc[2]['Team'],
           ALwc.iloc[0]['Team'], ALwc.iloc[1]['Team']]
    for i in NLplay:
        i.seed = 'N'+str(NLplay.index(i) + 1)
    for i in ALplay:
        i.seed = 'A'+str(ALplay.index(i) + 1)
    print('NL Playoffs')
    bracket(NLplay)
    print('AL Playoffs')
    bracket(ALplay)
    print('National League Wild Card')
    NLWC = series(NLplay[3], NLplay[4], 1)
    print('American League Wild Card')
    ALWC = series(ALplay[3], ALplay[4], 1)
    print('National League Division Series')
    NLDS1 = series(NLplay[0], NLWC, 3)
    NLDS2 = series(NLplay[1], NLplay[2], 3)
    print('American League Division Series')
    ALDS1 = series(ALplay[0], ALWC, 3)
    ALDS2 = series(ALplay[1], ALplay[2], 3)
    print('National League Championship Series')
    if NLplay.index(NLDS1) < NLplay.index(NLDS2):
        NLCS = series(NLDS1, NLDS2, 4)
    else:
        NLCS = series(NLDS2, NLDS1, 4)
    print('American League Championship Series')
    if ALplay.index(ALDS1) < ALplay.index(ALDS2):
        ALCS = series(ALDS1, ALDS2, 4)
    else:
        ALCS = series(ALDS2, ALDS1, 4)
    print('World Series')
    if WSHost == 'NL':
        WS = series(NLCS, ALCS, 4)
    else:
        WS = series(ALCS, NLCS, 4)
    print(WS, 'wins the world series!!!')


def playoffs8(NLs, ALs, WSHost):  # MLB 1994-2011
    NLdw = NLs.loc[NLs['D. Winner'] == True]
    ALdw = ALs.loc[ALs['D. Winner'] == True]
    NLwc = NLs.loc[NLs['D. Winner'] == False]
    ALwc = ALs.loc[ALs['D. Winner'] == False]
    NLplay = [NLdw.iloc[0]['Team'], NLdw.iloc[1]['Team'], NLdw.iloc[2]['Team'],
           NLwc.iloc[0]['Team']]
    ALplay = [ALdw.iloc[0]['Team'], ALdw.iloc[1]['Team'], ALdw.iloc[2]['Team'],
           ALwc.iloc[0]['Team']]
    for i in NLplay:
        i.seed = 'N'+str(NLplay.index(i) + 1)
    for i in ALplay:
        i.seed = 'A'+str(ALplay.index(i) + 1)
    print('NL Playoffs')
    bracket(NLplay)
    print('AL Playoffs')
    bracket(ALplay)
    print('National League Division Series')
    NLDS1 = series(NLplay[0], NLplay[3], 3)
    NLDS2 = series(NLplay[1], NLplay[2], 3)
    print('American League Division Series')
    ALDS1 = series(ALplay[0], ALplay[3], 3)
    ALDS2 = series(ALplay[1], ALplay[2], 3)
    print('National League Championship Series')
    if NLplay.index(NLDS1) < NLplay.index(NLDS2):
        NLCS = series(NLDS1, NLDS2, 4)
    else:
        NLCS = series(NLDS2, NLDS1, 4)
    print('American League Championship Series')
    if ALplay.index(ALDS1) < ALplay.index(ALDS2):
        ALCS = series(ALDS1, ALDS2, 4)
    else:
        ALCS = series(ALDS2, ALDS1, 4)
    print('World Series')
    if WSHost == 'NL':
        WS = series(NLCS, ALCS, 4)
    else:
        WS = series(ALCS, NLCS, 4)
    print(WS, 'wins the world series!!!')


def playoffsDP12(NLs, ALs):  # No one ever has thought this was a good idea
    NLdw = NLs.loc[NLs['D. Winner'] == True]
    ALdw = ALs.loc[ALs['D. Winner'] == True]
    NLwc = NLs.loc[NLs['D. Winner'] == False]
    ALwc = ALs.loc[ALs['D. Winner'] == False]
    NLplay = [NLdw.iloc[0]['Team'], NLdw.iloc[1]['Team'], NLdw.iloc[2]['Team'],
              NLwc.iloc[0]['Team'], NLwc.iloc[1]['Team'], NLwc.iloc[2]['Team']]
    ALplay = [ALdw.iloc[0]['Team'], ALdw.iloc[1]['Team'], ALdw.iloc[2]['Team'],
              ALwc.iloc[0]['Team'], ALwc.iloc[1]['Team'], ALwc.iloc[2]['Team']]
    for i in NLplay:
        i.seed = 'N'+str(NLplay.index(i) + 1)
    for i in ALplay:
        i.seed = 'A'+str(ALplay.index(i) + 1)
    bracket(NLplay+ALplay)
    print('WINNERS QF')
    G1 = series(NLplay[0], ALplay[3], 3, losers=True)
    G2 = series(ALplay[1], NLplay[2], 3, losers=True)
    G3 = series(ALplay[0], NLplay[3], 3, losers=True)
    G4 = series(NLplay[1], ALplay[2], 3, losers=True)
    print('LOSERS R1')
    G5 = series(G1[1], NLplay[4], 2, losers=True)
    G6 = series(G2[1], ALplay[5], 2, losers=True)
    G7 = series(G3[1], ALplay[4], 2, losers=True)
    G8 = series(G4[1], NLplay[5], 2, losers=True)
    print('WINNERS SF')
    G9 = series(G1[0], G2[0], 3, losers=True, wins=True)
    G10 = series(G3[0], G4[0], 3, losers=True, wins=True)
    print('LOSERS R2')
    G11 = series(G5[0], G6[0], 2, losers=True, wins=True)
    G12 = series(G7[0], G8[0], 2, losers=True, wins=True)
    print('LOSERS R3')
    G13 = series(G10[1], G11[0], 3, losers=True)
    G14 = series(G9[1], G12[0], 3, losers=True)
    print('WINNERS FINAL')
    G15 = series(G9[0], G10[0], 4, losers=True, wins=True)
    print('LOSERS SF')
    G16 = series(G13[0], G14[0], 3, losers=True, wins=True)
    print('LOSERS FINAL')
    G17 = series(G15[1], G16[0], 4, losers=True)
    print('WORLD SERIES')
    G18 = series(G15[0], G17[0], 4)
    if G18 == G15[0]:
        G19 = G18
    else:
        G19 = series(G17[0], G15[0], 4)  # Losers winner gets home field in the bracket reset I think is fair
    print(G19, 'WINS THE WORLD SERIES')


def hrDerby(NLcontestants, ALcontestants, host):
    print('National League Contestants')
    for i in NLcontestants:
        print(i.bigLine())
    print('American League Contestants')
    for i in ALcontestants:
        print(i.bigLine())
    board = Scoreboard(host.ABR, 1)
    print('National League SF')
    NL1 = hrdMatchup(NLcontestants[0], NLcontestants[3], board)
    NL2 = hrdMatchup(NLcontestants[1], NLcontestants[2], board)
    print('American League SF')
    AL1 = hrdMatchup(ALcontestants[0], ALcontestants[3], board)
    AL2 = hrdMatchup(ALcontestants[1], ALcontestants[2], board)
    print('National League Final')
    NLwinner = hrdMatchup(NL1, NL2, board)
    print('American League Final')
    ALwinner = hrdMatchup(AL1, AL2, board)
    print('Grand Final')
    winner = hrdMatchup(NLwinner, ALwinner, board)
    print(winner.team, winner.idLine(), 'WINS THE TITLE')


def hrdMatchup(x, y, board):
    print(x.team, x.idLine(), 'v', y.team, y.idLine())
    xScore = 0
    xOuts = 0
    yScore = 0
    yOuts = 0
    swings = 0
    while xOuts < 10:
        res = hrdPitch(x, board)
        if res == True:
            xScore += 1
        elif res == '':
            pass
        else:
            xOuts += 1
        swings += 1
        if board.p >= 2:
            print(xScore, xOuts)
    while yOuts < 10:
        res = hrdPitch(y, board)
        if res == True:
            yScore += 1
        elif res == '':
            pass
        else:
            yOuts += 1
        if board.p >= 2:
            print(yScore, yOuts)
    if xScore > yScore:
        print(x.team, x.idLine(), 'Wins!', str(xScore)+'-'+str(yScore))
        return x
    elif yScore > xScore:
        print(y.team, y.idLine(), 'Wins!', str(yScore)+'-'+str(xScore))
        return y
    else:
        swings = 0
        while swings < 3 or xScore == yScore:
            if hrdPitch(x, board) == True:
                xScore += 1
            if hrdPitch(y, board) == True:
                yScore += 1
            swings += 1
            if board.p >= 2:
                print(x, xScore, y, yScore)
        if xScore > yScore:
            print(x.team, x.idLine(), 'Wins!', str(xScore)+'-'+str(yScore), 'after', swings, 'extra swings')
            return x
        elif yScore > xScore:
            print(y.team, y.idLine(), 'Wins!', str(yScore)+'-'+str(xScore), 'after', swings, 'extra swings')
            return y


def allstarGame(gp):  # I thought it would be fun
    AShost = random.choice(MLBt)
    print('ALL-STAR WEEKEND HOSTED BY', AShost)
    (NLh, NLp, ALh, ALp) = buildPDFs()
    # Set up the stats
    NLp['IP'] = [i.IP for i in list(NLp['Name'])]
    NLp['ERA'] = [i.ERA for i in list(NLp['Name'])]
    ALp['IP'] = [i.IP for i in list(ALp['Name'])]
    ALp['ERA'] = [i.ERA for i in list(ALp['Name'])]
    NLh['PA'] = [i.PA for i in list(NLh['Name'])]
    NLh['OPS'] = [i.OPS for i in list(NLh['Name'])]
    NLh['HR'] = [i.HR for i in list(NLh['Name'])]
    ALh['PA'] = [i.PA for i in list(ALh['Name'])]
    ALh['OPS'] = [i.OPS for i in list(ALh['Name'])]
    ALh['HR'] = [i.HR for i in list(ALh['Name'])]
    # HR derby contestants
    NLh.sort_values(['HR', 'OPS'], inplace=True, ascending=False)
    ALh.sort_values(['HR', 'OPS'], inplace=True, ascending=False)
    nlHRD = NLh.iloc[0:4, 0]
    alHRD = ALh.iloc[0:4, 0]
    hrDerby(list(nlHRD), list(alHRD), AShost)
    # Now the real AS stuff
    NLh.sort_values(['OPS'], inplace=True, ascending=False)
    ALh.sort_values(['OPS'], inplace=True, ascending=False)
    NLp.sort_values(['ERA'], inplace=True, ascending=True)
    ALp.sort_values(['ERA'], inplace=True, ascending=True)
    # Set the lineups
    NLdefense = [None] * 10
    NLbatting = pandas.DataFrame(columns=['Name', 'Team', 'Position', 'Offense', 'OPS'])
    NLstarter = NLp[(NLp['IP'] > gp/2) & (NLp['Pos']=='SP')].iloc[0]['Name']
    NLbullpen = NLp[(NLp['IP'] > gp/2) & ~(NLp['Name']==NLstarter)].iloc[0:15]
    NLbullpen['Available'] = [True for i in range(len(NLbullpen))]
    NLdefense[1] = NLstarter
    for i in range(2, 10):
        cur = NLh[(NLh['Pos'] == posNotation[i]) & (NLh['PA'] >= 2*gp)].iloc[0]['Name']
        NLdefense[i] = cur
        NLbatting.loc[len(NLbatting)] = [cur, cur.team, posNotation[i], cur.offense, cur.OPS]
    NLdh = NLh[~(NLh['Name'].isin(NLdefense)) & (NLh['PA'] >= 2*gp)].iloc[0]['Name']
    NLdefense[0] = NLdh
    NLbatting.loc[len(NLbatting)] = [NLdh, NLdh.team, 'DH', NLdh.offense, NLdh.OPS]
    NLbatting.sort_values(['Offense', 'OPS'], ascending=False, inplace=True)
    NLAllStars = ASTeam('National League AS   ', 'NLA', NLdefense, NLbatting, NLbullpen)
    NLAllStars.lineupCard.closer = NLbullpen.iloc[0,0]
    NLAllStars.lineupCard.starters = pandas.concat([NLbatting, pandas.DataFrame([[NLstarter, NLstarter.team, 'SP',
        NLstarter.overall, NLstarter.ERA]], columns=['Name', 'Team', 'Position', 'Offense', 'OPS'])], ignore_index=True)
    # AL
    ALdefense = [None] * 10
    ALbatting = pandas.DataFrame(columns=['Name', 'Team', 'Position', 'Offense', 'OPS'])
    ALstarter = ALp[(ALp['IP'] > gp / 2) & (ALp['Pos'] == 'SP')].iloc[0]['Name']
    ALbullpen = ALp[(ALp['IP'] > gp / 2) & ~(ALp['Name'] == ALstarter)].iloc[0:15]
    ALbullpen['Available'] = [True for i in range(len(ALbullpen))]
    ALdefense[1] = ALstarter
    for i in range(2, 10):
        cur = ALh[(ALh['Pos'] == posNotation[i]) & (ALh['PA'] >= 2 * gp)].iloc[0]['Name']
        ALdefense[i] = cur
        ALbatting.loc[len(ALbatting)] = [cur, cur.team, posNotation[i], cur.offense, cur.OPS]
    ALdh = ALh[~(ALh['Name'].isin(ALdefense)) & (ALh['PA'] >= 2 * gp)].iloc[0]['Name']
    ALdefense[0] = ALdh
    ALbatting.loc[len(ALbatting)] = [ALdh, ALdh.team, 'DH', ALdh.offense, ALdh.OPS]
    ALbatting.sort_values(['Offense', 'OPS'], ascending=False, inplace=True)
    ALAllStars = ASTeam('American League AS   ', 'ALA', ALdefense, ALbatting, ALbullpen)
    ALAllStars.lineupCard.closer = ALbullpen.iloc[0, 0]
    ALAllStars.lineupCard.starters = pandas.concat([ALbatting, pandas.DataFrame([[ALstarter, ALstarter.team, 'SP',
        ALstarter.overall, ALstarter.ERA]],columns=['Name', 'Team', 'Position','Offense', 'OPS'])],ignore_index=True)
    # Play the game
    if AShost in NLt:
        ASTeams = [NLAllStars, ALAllStars]
        NLAllStars.hostABR = AShost.ABR
    else:
        ASTeams = [ALAllStars, NLAllStars]
        ALAllStars.hostABR = AShost.ABR
    for i in ASTeams:
        i.setTeam()
    game(ASTeams[0], ASTeams[1], p=2, stam=25)
    if NLAllStars.wins > 0:
        print('NATIONAL LEAGUE WINS')
        return 'NL'
    else:
        print('AMERICAN LEAGUE WINS')
        return 'AL'


def endOfYear(gp):
    (NLh, NLp, ALh, ALp) = buildPDFs()
    # pitchers
    NLp['IP'] = [i.IP for i in list(NLp['Name'])]
    NLp['ERA'] = [i.ERA for i in list(NLp['Name'])]
    NLp['W'] = [i.W for i in list(NLp['Name'])]
    NLp['S'] = [i.S for i in list(NLp['Name'])]
    NLp['K%'] = [i.Kp for i in list(NLp['Name'])]
    NLp['RA'] = [round(i.rAdded, 2) for i in list(NLp['Name'])]
    NLp['wRA'] = [i.wRA for i in list(NLp['Name'])]
    ALp['IP'] = [i.IP for i in list(ALp['Name'])]
    ALp['ERA'] = [i.ERA for i in list(ALp['Name'])]
    ALp['W'] = [i.W for i in list(ALp['Name'])]
    ALp['S'] = [i.S for i in list(ALp['Name'])]
    ALp['K%'] = [i.Kp for i in list(ALp['Name'])]
    ALp['RA'] = [round(i.rAdded, 2) for i in list(ALp['Name'])]
    ALp['wRA'] = [i.wRA for i in list(ALp['Name'])]
    # hitters
    NLh['PA'] = [i.PA for i in list(NLh['Name'])]
    NLh['HR'] = [i.HR for i in list(NLh['Name'])]
    NLh['OPS'] = [i.OPS for i in list(NLh['Name'])]
    NLh['SB'] = [i.SB for i in list(NLh['Name'])]
    NLh['SB%'] = [i.Sp for i in list(NLh['Name'])]
    NLh['RA'] = [round(i.rAdded, 2) for i in list(NLh['Name'])]
    NLh['wRC+'] = [i.wRCp for i in list(NLh['Name'])]
    ALh['PA'] = [i.PA for i in list(NLh['Name'])]
    ALh['HR'] = [i.HR for i in list(ALh['Name'])]
    ALh['OPS'] = [i.OPS for i in list(ALh['Name'])]
    ALh['SB'] = [i.SB for i in list(ALh['Name'])]
    ALh['SB%'] = [i.Sp for i in list(ALh['Name'])]
    ALh['RA'] = [round(i.rAdded, 2) for i in list(ALh['Name'])]
    ALh['wRC+'] = [i.wRCp for i in list(ALh['Name'])]
    print('End of year statistical leaders')
    print('Pitching-NL')
    NLp.sort_values(['IP'], inplace=True, ascending=False)
    print(NLp.head())
    NLp.sort_values(['ERA'], inplace=True, ascending=True)
    print(NLp[NLp['IP'] >= gp].head())
    NLp.sort_values(['W'], inplace=True, ascending=False)
    print(NLp.head())
    NLp.sort_values(['S'], inplace=True, ascending=False)
    print(NLp.head())
    NLp.sort_values(['K%'], inplace=True, ascending=False)
    print(NLp[NLp['IP'] >= gp].head())
    NLp.sort_values(['RA'], inplace=True, ascending=False)
    print(NLp.head())
    NLp.sort_values(['wRA'], inplace=True, ascending=True)
    print(NLp[NLp['IP'] >= gp].head())
    print('Pitching-AL')
    ALp.sort_values(['IP'], inplace=True, ascending=False)
    print(ALp.head())
    ALp.sort_values(['ERA'], inplace=True, ascending=True)
    print(ALp[ALp['IP'] >= gp].head())
    ALp.sort_values(['W'], inplace=True, ascending=False)
    print(ALp.head())
    ALp.sort_values(['S'], inplace=True, ascending=False)
    print(ALp.head())
    ALp.sort_values(['K%'], inplace=True, ascending=False)
    print(ALp[ALp['IP'] >= gp].head())
    ALp.sort_values(['RA'], inplace=True, ascending=False)
    print(ALp.head())
    ALp.sort_values(['wRA'], inplace=True, ascending=True)
    print(ALp[ALp['IP'] >= gp].head())
    print('Hitting-NL')
    NLh.sort_values(['OPS'], inplace=True, ascending=False)
    print(NLh[NLh['PA'] >= 3*gp].head())
    NLh.sort_values(['HR'], inplace=True, ascending=False)
    print(NLh.head())
    NLh.sort_values(['SB'], inplace=True, ascending=False)
    print(NLh.head())
    NLh.sort_values(['RA'], inplace=True, ascending=False)
    print(NLh.head())
    NLh.sort_values(['wRC+'], inplace=True, ascending=False)
    print(NLh[NLh['PA'] >= 3*gp].head())
    print('Hitting-AL')
    ALh.sort_values(['OPS'], inplace=True, ascending=False)
    print(ALh[ALh['PA'] >= 3*gp].head())
    ALh.sort_values(['HR'], inplace=True, ascending=False)
    print(ALh.head())
    ALh.sort_values(['SB'], inplace=True, ascending=False)
    print(ALh.head())
    ALh.sort_values(['RA'], inplace=True, ascending=False)
    print(ALh.head())
    ALh.sort_values(['wRC+'], inplace=True, ascending=False)
    print(ALh[ALh['PA'] >= 3*gp].head())
    for i in MLBt:
        if i.controlled:
            print('Your Team')
            for j in i.hitters['Name']:
                print(j.bigLine())
            for j in i.rotation['Name']:
                print(j.bigLine())
            for j in i.bullpen['Name']:
                print(j.bigLine())
    #gameplayEOY()


def bracket(teams):  # Derpy as hell but I like how it looks this way
    if len(teams) == 8:
        print(teams[0].ABR + '|')
        print('   |____')
        print(teams[7].ABR + '|    |')
        print('        |____')
        print(teams[3].ABR + '|    |    |')
        print('   |____|    |')
        print(teams[4].ABR + '|         |')
        print('             |___')
        print(teams[1].ABR + '|         |')
        print('   |____     |')
        print(teams[6].ABR + '|    |    |')
        print('        |____|')
        print(teams[2].ABR + '|    |')
        print('   |____|')
        print(teams[5].ABR + '|')
    elif len(teams) == 6:
        print('     ' + teams[0].ABR+'|')
        print('        |____')
        print(teams[3].ABR + '|    |    |')
        print('   |____|    |')
        print(teams[4].ABR + '|         |____')
        print('     ' + teams[1].ABR+'|    |')
        print('        |____|')
        print(teams[2].ABR + '|    |')
        print('   |____|')
        print(teams[5].ABR + '|')
    elif len(teams) == 5:
        print('     ' + teams[0].ABR + '|')
        print('        |____')
        print(teams[3].ABR + '|    |    |')
        print('   |____|    |')
        print(teams[4].ABR + '|         |____')
        print('     ' + teams[1].ABR + '|    |')
        print('        |____|')
        print('     '+teams[2].ABR+'|')
    elif len(teams) == 4:
        print(teams[0].ABR + '|')
        print('   |____')
        print(teams[3].ABR + '|    |')
        print('        |____')
        print(teams[2].ABR + '|    |')
        print('   |____|')
        print(teams[3].ABR + '|')
    elif len(teams) == 12:
        print('WINNERS BRACKET')
        print(teams[0].ABR + '|')
        print('   |____')
        print(teams[9].ABR + '|    |')
        print('        |____')
        print(teams[7].ABR + '|    |    |')
        print('   |____|    |')
        print(teams[2].ABR + '|         |')
        print('             |___')
        print(teams[6].ABR + '|         |')
        print('   |____     |')
        print(teams[3].ABR + '|    |    |')
        print('        |____|')
        print(teams[1].ABR + '|    |')
        print('   |____|')
        print(teams[8].ABR + '|')
        print('LOSERS BRACKET')
        print('___|')
        print('   |____')
        print(teams[4].ABR + '|')
        print()
        print('___|')
        print('   |____')
        print(teams[11].ABR + '|')
        print()
        print('___|')
        print('   |____')
        print(teams[10].ABR + '|')
        print()
        print('___|')
        print('   |____')
        print(teams[5].ABR + '|')


def offseason(year, p, holdovers):
    freeAgents = pandas.DataFrame(columns=['Name', 'Pos1', 'Pos2', 'Age', 'Core', 'OVR', 'Value'])
    pDeals = 0
    full = True if year <= simYears else False
    for i in NLt+ALt:
        teamFAs = i.reset()
        freeAgents = pandas.concat([freeAgents, teamFAs], ignore_index=True)
        i.prospectsAvailable(full)
        if not full and i.controlled:
            i.needCheck()
            print(*i.needs)
    if not full:
        prospectDraft(p)
    for i in MLBt:
        i.prospects.sort_values(['Value'], inplace=True, ascending=False, ignore_index=True)
    if faFormat == 1:  # EXCEL THING
        freeAgents = pandas.concat([freeAgents, holdovers])
        go = True
        roundNum = 0
        while go:
            if roundNum > 10:
                p = 2
            if p > 0:
                print('ROUND', roundNum+1)
            go = False
            for i in NLt+ALt:
                i.needCheck()
                if i.needs[0] > 0 or i.needs[2] > 0 or i.needs[3] > 0:
                    go = True
                    if p > 1:
                        print(i.ABR, *i.needs)
                    i.contractBundle(freeAgents, roundNum, year, p)
            if p > 0:
                print('Prospect Deals')
            for i in NLt + ALt:
                for j in i.prospects['Name']:
                    sign = j.acceptDeal()
                    if sign is not None:
                        pDeals += 1
                        if isinstance(j, Hitter) and p > 0:
                            print(j.pos + '/' + j.secondary, j.smallLine(), 'signs with', sign[0], 'for', sign[1], 'years',
                                  sign[2], 'AAV')
                        elif p > 0:
                            print(j.pos+'   ', j.smallLine(), 'signs with', sign[0], 'for', sign[1], 'years', sign[2], 'AAV')
                        i.prospects.drop(i.prospects[i.prospects['Name'] == j].index, inplace=True)
                        i.prospects.reset_index(drop=True, inplace=True)
            if p > 0:
                print('FA Deals')
            for i in freeAgents['Name']:
                sign = i.acceptDeal()
                if sign is not None:
                    if isinstance(i, Hitter) and p > 0:
                        print(i.idLine(), 'signs with', sign[0], 'for', sign[1], 'years', sign[2], 'AAV')
                    elif p > 0:
                        print(i.idLine(), 'signs with', sign[0], 'for', sign[1], 'years', sign[2], 'AAV')
                    freeAgents.drop(freeAgents[freeAgents['Name'] == i].index, inplace=True)
            roundNum += 1
        if p > 0:
            print('FREE AGENCY IS DONE AFTER', roundNum-1, 'ROUNDS')
    else:
        freeAgents.sort_values(['Core', 'OVR'], inplace=True, ignore_index=True, ascending=False)
        #with alive_bar(len(freeAgents), dual_line=True, title='FAs') as bar:
        if p == 0:
            for i in alive_it(range(len(freeAgents))):
                if auctionHelperThing(freeAgents, i, p, year):
                    break
        else:
            for i in range(len(freeAgents)):
                if auctionHelperThing(freeAgents, i, p, year):
                    break
        if p >= 1:
            print('FILL-IN')
        for j in MLBt:
            j.fillIn(p)
    for i in NLt+ALt:
        i.hitters.sort_values(['Overall', 'Offense'], inplace=True, ascending=False)
        i.rotation.sort_values(['Core', 'Extension'], inplace=True, ascending=False)
        i.bullpen.sort_values(['Core', 'Extension'], inplace=True, ascending=False)
        i.setTeam()
        i.lineupCard = Lineup(i.rotation, i.hitters, i.ABR)
        i.lineupCard.closer = i.bullpen.iloc[0, 0]
    if p > 0 and faFormat == 1:
        print(len(freeAgents[freeAgents['Age'] >= 8]), 'have retired')
    elif p > 0:
        print(len(freeAgents), 'have retired')
    return freeAgents[freeAgents['Age'] < 8]


def prospectDraft(p):
    draftOrder = pandas.DataFrame(columns=['Team', 'Previous Wins'])
    for i in MLBt:
        draftOrder.loc[len(draftOrder)] = [i, i.prevWins]
    draftOrder.sort_values(['Previous Wins'], inplace=True, ignore_index=True, ascending=True)
    print(draftOrder)
    prospects = pandas.DataFrame(columns=['Name', 'Pos1', 'Pos2', 'Age', 'Core', 'OVR', 'Value'])
    for i in range(30*draftDepth):
        inf = Hitter(nameGen(), random.choice(infieldPos), hand=random.choice(hitterHand), top=8)
        inf.age = 1
        inf.secondary = random.choice(infieldPos)
        prospects.loc[len(prospects)] = [inf, inf.pos, inf.secondary, 1, inf.offense, inf.overall, 0]
    for i in range(30*draftDepth):
        out = Hitter(nameGen(), random.choice(outfieldPos), hand=random.choice(hitterHand), top=8)
        out.age = 1
        out.secondary = random.choice(outfieldPos)
        prospects.loc[len(prospects)] = [out, out.pos, out.secondary, 1, out.offense, out.overall, 0]
    for i in range(30*min(draftDepth, 3)):
        sp = Pitcher(nameGen(), 'SP', hand=random.choice(pitcherHand), top=8)
        sp.age = 1
        prospects.loc[len(prospects)] = [sp, 'SP', numpy.nan, 1, sp.overall, sp.total, 0]
    for i in range(30*draftDepth):
        rp = Pitcher(nameGen(), 'RP', hand=random.choice(pitcherHand), top=8)
        rp.age = 1
        prospects.loc[len(prospects)] = [rp, 'RP', numpy.nan, 1, rp.overall, rp.total, 0]
    if p > 0:
        print('Welcome to the Prospect Draft!!')
    for i in range(min(4*draftDepth, 15)):
        print(f'ROUND {i+1}')
        for j in range(30):
            team = draftOrder.loc[j, 'Team']
            pick = team.prospectDrafter(prospects, )
            prospects.drop(prospects[prospects['Name'] == pick].index, inplace=True)
            if p > 0:
                print(f'Pick {i+1}.{j+1}: {team.ABR} selects {pick.idLine()}')


def auctionHelperThing(freeAgents, i, p, year):
    # if i%20 == 0:
    # print(str(i)+'/'+str(len(freeAgents)))
    if i > 125 and i % 5 == 0:
        if areWeDone():
            print('stopping early at', i)
            return True
    prospectsOffered = []
    player = freeAgents.loc[i, 'Name']
    if p >= 1:
        print('PLAYER IS:', player.idLine())
    for j in MLBt:
        if j.controlled:
            if i == 0:
                j.next = 0
            if j.next == i:
                offer = j.selfAuction(freeAgents, player, p, year)
            else:
                offer = None
            if j.next == i:
                j.next += 1
        else:
            offer = j.auction(player, p, year)
        if offer is not None:
            if offer != player:
                prospectsOffered.append(offer)
    for k in [player] + prospectsOffered:
        sign = k.acceptDeal()
        if sign is not None:
            if isinstance(k, Hitter) and p > 0:
                print(k.idLine(), 'signs with', sign[0], 'for', sign[1], 'years', sign[2], 'AAV')
            elif p > 0:
                print(k.idLine(), 'signs with', sign[0], 'for', sign[1], 'years', sign[2], 'AAV')
            if k == player:
                freeAgents.drop(freeAgents[freeAgents['Name'] == i].index, inplace=True)
            sign[0].needCheck()
            if p >= 2:
                print(sign[0], 'has remaining budget of', sign[0].budgetRemaining(year), round(sign[0].hitterCon, 1),
                      round(sign[0].spCon, 1), round(sign[0].rpCon, 1), *sign[0].needs)
    return False


def areWeDone():
    for i in MLBt:
        if len(i.hitters) < 13 or len(i.rotation) < 5 or len(i.bullpen) < 8:
            return False
    return True


def holdUpdate(holdovers):
    res = pandas.DataFrame(columns=['Name', 'Pos1', 'Pos2', 'Age', 'Core', 'OVR', 'Value'])
    for i in holdovers['Name']:
        i.age += 1
        i.boost(ageCurve(i.age, i.controlled))
        if isinstance(i, Hitter):
            res.loc[len(res)] = [i, i.pos, i.secondary, i.age, i.offense, i.overall, 0]
        else:
            res.loc[len(res)] = [i, i.pos, i.secondary, i.age, i.overall, i.total, 0]
    return res


def buildPDFs():
    # Build DFs of all hitters and pitchers for each league for AS selection and EOY awards
    NLh = pandas.DataFrame(columns=['Name', 'Pos', 'OVR', 'Team'])  # NL Hitters
    NLp = pandas.DataFrame(columns=['Name', 'Pos', 'OVR', 'Team'])  # NL Pitchers
    ALh = pandas.DataFrame(columns=['Name', 'Pos', 'OVR', 'Team'])
    ALp = pandas.DataFrame(columns=['Name', 'Pos', 'OVR', 'Team'])
    for i in NLt:
        for j in i.hitters['Name']:
            j.team = i.ABR
            NLh.loc[len(NLh)] = [j, j.pos, j.offense, i.ABR]
    for i in NLt:
        for j in i.rotation['Name']:
            j.team = i.ABR
            NLp.loc[len(NLp)] = [j, 'SP', j.overall, i.ABR]
        for j in i.bullpen['Name']:
            j.team = i.ABR
            NLp.loc[len(NLp)] = [j, 'RP', j.overall, i.ABR]
    for i in ALt:
        for j in i.hitters['Name']:
            j.team = i.ABR
            ALh.loc[len(ALh)] = [j, j.pos, j.offense, i.ABR]
    for i in ALt:
        for j in i.rotation['Name']:
            j.team = i.ABR
            ALp.loc[len(ALp)] = [j, 'SP', j.overall, i.ABR]
        for j in i.bullpen['Name']:
            j.team = i.ABR
            ALp.loc[len(ALp)] = [j, 'RP', j.overall, i.ABR]
    return (NLh, NLp, ALh, ALp)


# Different League Format
def format2():
    random.shuffle(MLBt)
    for dkajfhdkfh in MLBt:  # i got annoyed
        dkajfhdkfh.setTeam()
    group1A = MLBt[0:5]
    group1B = MLBt[5:10]
    group1C = MLBt[10:15]
    group1D = MLBt[15:20]
    group1E = MLBt[20:25]
    group1F = MLBt[25:30]
    groups1 = [group1A, group1B, group1C, group1D, group1E, group1F]
    gNames = ['Group A', 'Group B', 'Group C', 'Group D', 'Group E', 'Group F']
    schedule = roundRobin(groups1)
    print('ROUND 1')
    R11 = [None] * 6
    R12 = [None] * 6
    R13 = [None] * 6
    R14 = [None] * 6
    R15 = [None] * 6
    for i in range(6):
        curStandings = pandas.DataFrame({'Team':groups1[i], 'Wins':[0]*5, 'RD':[0]*5})
        print(gNames[i])
        print(curStandings)
        curSched = schedule[i*5:i*5 + 5]
        for j in curSched:
            for k in j:
                if k[0] and k[1]:
                    game(k[0], k[1], p=1)
        for j in curSched:
            for k in j:
                if k[0] and k[1]:
                    game(k[1], k[0], p=1)
        curStandings['Wins'] = [z.wins for z in curStandings['Team']]
        curStandings['RD'] = [z.runsFor - z.runsAgainst for z in curStandings['Team']]
        curStandings.sort_values(['Wins', 'RD'], ascending=False, inplace=True, ignore_index=True)
        print(curStandings)
        R11[i] = curStandings.iloc[0].Team
        R12[i] = curStandings.iloc[1].Team
        R13[i] = curStandings.iloc[2].Team
        R14[i] = curStandings.iloc[3].Team
        R15[i] = curStandings.iloc[4].Team
    print('Advanced:', *R11)  # 6/6 advance from here
    print(*R12)  # 4/6 advance from here
    print(*R13)  # 3/6 advance from here
    print(*R14)  # 2/6 advance from here
    print('Eliminated:', *R15)  # 0/6 advance from here
    for i in MLBt:
        i.softReset()
    print('ROUND 2')
    groups2 = [R12, R13, R14]
    gNames2 = ['Second Place (4 Advance)', 'Third Place (3 Advance)', 'Fourth Place (2 Advance)']
    schedule2 = roundRobin(groups2)
    R2A = []
    R2E = []
    for i in range(3):
        curStandings = pandas.DataFrame({'Team':groups2[i], 'Wins':[0]*6, 'RD':[0]*6})
        print(gNames2[i])
        print(curStandings)
        curSched = schedule2[i*5:i*5 + 5]
        for j in curSched:
            for k in j:
                if k[0] and k[1]:
                    game(k[0], k[1], p=1)
        for j in curSched:
            for k in j:
                if k[0] and k[1]:
                    game(k[1], k[0], p=1)
        curStandings['Wins'] = [z.wins for z in curStandings['Team']]
        curStandings['RD'] = [z.runsFor - z.runsAgainst for z in curStandings['Team']]
        curStandings.sort_values(['Wins', 'RD'], ascending=False, inplace=True, ignore_index=True)
        print(curStandings)
        for j in range(6):
            if j < 4-i:
                R2A.append(curStandings.iloc[j].Team)
            else:
                R2E.append(curStandings.iloc[j].Team)
    print(*R2A)
    print('Eliminated:', *R2E)
    R3 = R2A + R11
    for i in R3:
        i.softReset()
    random.shuffle(R2A)
    group3A = R3[0:5]
    group3B = R3[5:10]
    group3C = R3[10:15]
    groups3 = [group3A, group3B, group3C]
    gNames3 = ['Group A', 'Group B', 'Group C']
    schedule3 = roundRobin(groups3)
    print('ROUND 3')
    R31 = [None] * 3
    R32 = [None] * 3
    R33 = [None] * 3
    R34 = [None] * 3
    R35 = [None] * 3
    for i in range(3):
        curStandings = pandas.DataFrame({'Team':groups3[i], 'Wins':[0]*5, 'RD':[0]*5})
        print(gNames3[i])
        print(curStandings)
        curSched = schedule3[i*5:i*5 + 5]
        for j in curSched:
            for k in j:
                if k[0] and k[1]:
                    game(k[0], k[1], p=1)
        for j in curSched:
            for k in j:
                if k[0] and k[1]:
                    game(k[1], k[0], p=1)
        curStandings['Wins'] = [z.wins for z in curStandings['Team']]
        curStandings['RD'] = [z.runsFor - z.runsAgainst for z in curStandings['Team']]
        curStandings.sort_values(['Wins', 'RD'], ascending=False, inplace=True, ignore_index=True)
        print(curStandings)
        R31[i] = curStandings.iloc[0].Team
        R32[i] = curStandings.iloc[1].Team
        R33[i] = curStandings.iloc[2].Team
        R34[i] = curStandings.iloc[3].Team
        R35[i] = curStandings.iloc[4].Team
    print('Advanced:', *R31)  # 3/3 advance from here
    print('Advanced:', *R32)  # 3/3 advance from here
    print(*R33)  # 1-2/3 advance from here
    print(*R34)  # 1-2/3 advance from here
    print('Eliminated:', *R35)  # 0/3 advance from here
    print('ROUND 4')
    group4 = R33 + R34
    for i in group4:
        i.softReset()
    R4A = []
    R4E = []
    schedule4 = roundRobin([group4])
    curStandings = pandas.DataFrame({'Team': group4, 'Wins': [0] * 6, 'RD': [0] * 6})
    print(curStandings)
    for j in schedule4:
        for k in j:
            if k[0] and k[1]:
                game(k[0], k[1], p=1)
    for j in schedule4:
        for k in j:
            if k[0] and k[1]:
                game(k[1], k[0], p=1)
    curStandings['Wins'] = [z.wins for z in curStandings['Team']]
    curStandings['RD'] = [z.runsFor - z.runsAgainst for z in curStandings['Team']]
    curStandings.sort_values(['Wins', 'RD'], ascending=False, inplace=True, ignore_index=True)
    print(curStandings)
    for i in range(6):
        if i < 2:
            R4A.append(curStandings.iloc[i].Team)
        else:
            R4E.append(curStandings.iloc[i].Team)
    print(*R4A)
    print('Eliminated:', *R4E)
    print('ROUND 5')
    R5 = R4A + R31 + R32
    for i in R5:
        i.softReset()
    random.shuffle(R5)
    group5A = R5[0:4]
    group5B = R5[4:8]
    groups5 = [group5A, group5B]
    gNames5 = ['Group A', 'Group B']
    schedule5 = roundRobin(groups5)
    R5A = []
    R5E = []
    for i in range(2):
        curStandings = pandas.DataFrame({'Team': groups5[i], 'Wins': [0] * 4, 'RD': [0] * 4})
        print(gNames5[i])
        print(curStandings)
        curSched = schedule5[i * 3:i * 3 + 3]
        for j in curSched:
            for k in j:
                if k[0] and k[1]:
                    game(k[0], k[1], p=1)
        for j in curSched:
            for k in j:
                if k[0] and k[1]:
                    game(k[1], k[0], p=1)
        curStandings['Wins'] = [z.wins for z in curStandings['Team']]
        curStandings['RD'] = [z.runsFor - z.runsAgainst for z in curStandings['Team']]
        curStandings.sort_values(['Wins', 'RD'], ascending=False, inplace=True, ignore_index=True)
        print(curStandings)
        for j in range(4):
            if j == 0:
                R5A.append(curStandings.iloc[j].Team)
            else:
                R5E.append(curStandings.iloc[j].Team)
    print(*R5A)
    print('Eliminated:', *R5E)
    print('ROUND 6/WORLD SERIES')
    random.shuffle(R5A)
    WS = series(R5A[0], R5A[1], 4)
    print(WS, 'WINS THE WORLD SERIES!!!')
    endOfYear(15)







