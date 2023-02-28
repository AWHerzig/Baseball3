from Gameplay import *
from Team import *
from DirectoryWide import *
import numpy

schedLength = '20'  # 0 is 20, 1 and '' is 52, 2 is 162
playoffSize = 'DE'  # 0 is 8, 1 is 10, 2 and '' is 12 (also 'DE12' for the fun one I'm gonna make)


def test(hScore, pScore):  # Sims a bunch of innings and returns a stat like ERA or OPS (currently ERA)
    # Offense
    board = Scoreboard('STL')  # Busch Field is just like a fairly average park
    hitter = Hitter(nameGen(), 'H ')
    (hitter.con, hitter.pow, hitter.vis, hitter.field, hitter.speed) = (hScore, hScore, hScore, hScore, hScore)
    oLineup = Lineup(None)
    oLineup.dAlign = [hitter]*10
    for i in range(9):
        oLineup.battingOrder.loc[len(oLineup.battingOrder)] = [hitter, 'H ', hScore*3, hitter.OPS]
    # Defense
    pitcher = Pitcher(nameGen(), 'P ')
    (pitcher.cont, pitcher.velo, pitcher.move, pitcher.field, pitcher.speed) = (pScore, pScore, pScore, pScore, pScore)
    dlineup = Lineup(None)
    dlineup.dAlign = [pitcher] * 10
    for i in range(1000):
        if i%100 == 0 and i>0:
            #print(i)
            pass
        #print('new inning')
        dlineup.dAlign[1].stamScore = 1000
        inning(oLineup, dlineup, board, 0)
    hitter.calcStats()
    pitcher.calcStats()
    #print('Hitter:', hScore, 'Pitcher:', pScore)
    #print(hitter.PA, hitter.slash, hitter.OPS, hitter.HR, hitter.Sp)
    #print(pitcher.BF, pitcher.IP, pitcher.ERA, pitcher.WHIP, pitcher.Kp)
    return pitcher.ERA


def test2(hScore, pScore):  # Sims a bunch of PAs and returns breakdown of results
    # Offense
    board = Scoreboard('STL')
    hitter = Hitter(nameGen(), 'H ')
    (hitter.con, hitter.pow, hitter.vis, hitter.field, hitter.speed) = (hScore, hScore, hScore, hScore, hScore)
    oLineup = Lineup(None)
    oLineup.dAlign = [hitter] * 10
    for i in range(9):
        oLineup.battingOrder.loc[len(oLineup.battingOrder)] = [hitter, 'H ', hScore * 3, hitter.OPS]
    # Defense
    pitcher = Pitcher(nameGen(), 'P ')
    (pitcher.cont, pitcher.velo, pitcher.move, pitcher.field, pitcher.speed) = (pScore, pScore, pScore, pScore, pScore)
    dlineup = Lineup(None)
    dlineup.dAlign = [pitcher] * 10
    K = 0
    BB = 0
    HR = 0
    S = 0
    D = 0
    T = 0
    IPHR = 0
    outs = 0
    for i in range(10000):
        board.refresh()
        board.pitcher = pitcher
        board.hitter = hitter
        hitter.chargedTo = pitcher
        res = PA(dlineup.dAlign, hitter, board, 0)
        if res == 'K':
            K += 1
        elif res == 'BB':
            BB += 1
        elif res == 'Home Run':
            HR += 1
        elif res[1] == 'single':
            S += 1
        elif res[1] == 'double':
            D += 1
        elif res[1] == 'triple':
            T += 1
        elif res[1] == 'IPHR':
            IPHR += 1
        elif res[1] == 'out':
            outs += 1
        else:
            print(res, 'bruh')
    AVG = (HR+S+D+T+IPHR) / (10000 - BB)
    OBP = (HR+S+D+T+IPHR+BB) / 10000
    SLG = ((4*HR)+S+(2*D)+(3*T)+(4*IPHR)) / (10000 - BB)
    return [int(K), int(BB), int(HR), int(S), int(D), int(T), int(IPHR), int(outs), int(OBP * 1000), int(SLG * 1000)]


seriesHome = [None, [0], [0, 0, 0], [0, 0, 1, 1, 0], [0, 0, 1, 1, 1, 0, 0]]
# First index is series length (in wins needed), second index: 0 means better seed hosts game, 1 means worse seed

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
Leagues = [NLt, ALt]
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


def series(top, bot, l, pri=1, losers=False, wins=False):  # Top seed, bottom seed, games needed to win, print value
    if wins:
        if bot.wins > top.wins:  # We are going to flip em
            hold = bot
            bot = top
            top = hold
    print(top.seed, top, 'vs.', bot.seed, bot, 'best of', (l*2) - 1)
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
        if i == len(schedule)//2:
            print('HALFWAY STANDINGS')
            for k in Standings:
                k['Played'] = [j.played for j in k['Team']]
                k['Wins'] = [j.wins for j in k['Team']]
                k['Losses'] = k['Played'] - k['Wins']
                k['Run D'] = [(j.runsFor - j.runsAgainst) for j in k['Team']]
                k.sort_values(['Wins', 'Run D'], inplace=True, ascending=False)  # irl tiebreak is H2H
                print(k)
            print('ALL-STAR BREAK')
            WSHost = allstarGame(NLp, NLh, ALp, ALh, int(schedLength)//2)  # Winner of the ASG gets top seed in WS
        print('SLATE', i+1)
        for j in schedule[i]:
            if j[0] and j[1]:
                game(j[0], j[1], p=0)
    endOfYear(NLp, NLh, ALp, ALh, int(schedLength))  # Stats Leaders
    print('DIVISION STANDINGS')
    for i in Standings:
        i['Played'] = [j.played for j in i['Team']]
        i['Wins'] = [j.wins for j in i['Team']]
        i['Losses'] = i['Played'] - i['Wins']
        i['Run D'] = [(j.runsFor - j.runsAgainst) for j in i['Team']]
        i.sort_values(['Wins', 'Run D'], inplace=True, ascending=False)
        i.iloc[0]['Team'].winDivision = True  # Secures playoff spot
        print(i)
    NLs = pandas.concat([NLEs, NLCs, NLWs])
    NLs['D. Winner'] = [j.winDivision for j in NLs['Team']]
    NLs.sort_values(['Wins', 'Run D'], inplace=True, ascending=False)
    ALs = pandas.concat([ALEs, ALCs, ALWs])
    ALs['D. Winner'] = [j.winDivision for j in ALs['Team']]
    ALs.sort_values(['Wins', 'Run D'], inplace=True, ascending=False)
    print('LEAGUE STANDINGS')
    print(NLs)
    print(ALs)
    if playoffSize in ['0', '8']:
        playoffs8(NLs, ALs, WSHost)
    elif playoffSize in ['1', '10']:
        playoffs10(NLs, ALs, WSHost)
    elif playoffSize in ['', '2', '12']:
        playoffs12(NLs, ALs, WSHost)
    elif playoffSize in ['DE', 'DE12']:
        playoffsDP12(NLs, ALs)
    else:
        print('whoop')


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
        WS = series(NLCS, ALCS, 4, pri=2)
    else:
        WS = series(ALCS, NLCS, 4, pri=2)
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
        WS = series(NLCS, ALCS, 4, pri=2)
    else:
        WS = series(ALCS, NLCS, 4, pri=2)
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
        WS = series(NLCS, ALCS, 4, pri=2)
    else:
        WS = series(ALCS, NLCS, 4, pri=2)
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
    G18 = series(G15[0], G17[0], 4, pri=2)
    if G18 == G15[0]:
        G19 = G18
    else:
        G19 = series(G17[0], G15[0], 4, pri=2)  # Losers winner gets home field in the bracket reset I think is fair
    print(G19, 'WINS THE WORLD SERIES')



def allstarGame(NLp, NLh, ALp, ALh, gp):  # I thought it would be fun
    # Set up the stats
    NLp['IP'] = [i.IP for i in list(NLp['Name'])]
    NLp['ERA'] = [i.ERA for i in list(NLp['Name'])]
    ALp['IP'] = [i.IP for i in list(ALp['Name'])]
    ALp['ERA'] = [i.ERA for i in list(ALp['Name'])]
    NLh['PA'] = [i.PA for i in list(NLh['Name'])]
    NLh['OPS'] = [i.OPS for i in list(NLh['Name'])]
    ALh['PA'] = [i.PA for i in list(NLh['Name'])]
    ALh['OPS'] = [i.OPS for i in list(NLh['Name'])]
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
    # Play the game
    ASTeams = [NLAllStars, ALAllStars]
    random.shuffle(ASTeams)
    game(ASTeams[0], ASTeams[1], p=2)
    if NLAllStars.wins > 0:
        print('NATIONAL LEAGUE WINS')
        return 'NL'
    else:
        print('AMERICAN LEAGUE WINS')
        return 'AL'


def endOfYear(NLp, NLh, ALp, ALh, gp):
    NLp['IP'] = [i.IP for i in list(NLp['Name'])]
    NLp['ERA'] = [i.ERA for i in list(NLp['Name'])]
    NLp['WHIP'] = [i.WHIP for i in list(NLp['Name'])]
    NLp['K%'] = [i.Kp for i in list(NLp['Name'])]
    ALp['IP'] = [i.IP for i in list(ALp['Name'])]
    ALp['ERA'] = [i.ERA for i in list(ALp['Name'])]
    ALp['WHIP'] = [i.WHIP for i in list(ALp['Name'])]
    ALp['K%'] = [i.Kp for i in list(ALp['Name'])]
    NLh['PA'] = [i.PA for i in list(NLh['Name'])]
    NLh['HR'] = [i.HR for i in list(NLh['Name'])]
    NLh['OPS'] = [i.OPS for i in list(NLh['Name'])]
    NLh['SB'] = [i.SB for i in list(NLh['Name'])]
    NLh['SB%'] = [i.Sp for i in list(NLh['Name'])]
    ALh['PA'] = [i.PA for i in list(NLh['Name'])]
    ALh['HR'] = [i.HR for i in list(ALh['Name'])]
    ALh['OPS'] = [i.OPS for i in list(ALh['Name'])]
    ALh['SB'] = [i.SB for i in list(ALh['Name'])]
    ALh['SB%'] = [i.Sp for i in list(ALh['Name'])]
    print('End of year statistical leaders')
    print('Pitching-NL')
    NLp.sort_values(['IP'], inplace=True, ascending=False)
    print(NLp[NLp['IP'] >= gp].head())
    NLp.sort_values(['ERA'], inplace=True, ascending=True)
    print(NLp[NLp['IP'] >= gp].head())
    NLp.sort_values(['WHIP'], inplace=True, ascending=True)
    print(NLp[NLp['IP'] >= gp].head())
    NLp.sort_values(['K%'], inplace=True, ascending=False)
    print(NLp[NLp['IP'] >= gp].head())
    print('Pitching-AL')
    ALp.sort_values(['IP'], inplace=True, ascending=False)
    print(ALp[ALp['IP'] >= gp].head())
    ALp.sort_values(['ERA'], inplace=True, ascending=True)
    print(ALp[ALp['IP'] >= gp].head())
    ALp.sort_values(['WHIP'], inplace=True, ascending=True)
    print(ALp[ALp['IP'] >= gp].head())
    ALp.sort_values(['K%'], inplace=True, ascending=False)
    print(ALp[ALp['IP'] >= gp].head())
    print('Hitting-NL')
    NLh.sort_values(['OPS'], inplace=True, ascending=False)
    print(NLh[NLh['PA'] >= 3*gp].head())
    NLh.sort_values(['HR'], inplace=True, ascending=False)
    print(NLh[NLh['PA'] >= 3*gp].head())
    NLh.sort_values(['SB'], inplace=True, ascending=False)
    print(NLh[NLh['PA'] >= 3*gp].head())
    print('Hitting-AL')
    ALh.sort_values(['OPS'], inplace=True, ascending=False)
    print(ALh[ALh['PA'] >= 3*gp].head())
    ALh.sort_values(['HR'], inplace=True, ascending=False)
    print(ALh[ALh['PA'] >= 3*gp].head())
    ALh.sort_values(['SB'], inplace=True, ascending=False)
    print(ALh[ALh['PA'] >= 3*gp].head())


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


def offseason():
    freeAgents = pandas.DataFrame(columns=['Name', 'Pos1', 'pos2', 'Age', 'Core', 'OVR'])
    for i in NLt+ALt:
        teamFAs = i.reset()
        freeAgents = pandas.concat([freeAgents, teamFAs])
    print(freeAgents)
    for i in NLt+ALt:
        print(i.ABR, *i.needCheck())








