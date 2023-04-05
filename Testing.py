import random

import pandas
from Players import *
from Team import *
from Gameplay import *
from DirectoryWide import *
import numpy


def bigtest():  # Each level of hitter plays each level of pitcher and returns some stat, usually ERA or OPS
    testing = pandas.DataFrame(columns=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
    for i in range(11):
        print('Round', i)
        testing.loc[len(testing)] = [test(i, j) for j in range(11)]
    print('hitter is row, pitcher is column')
    print(testing)


def bigtest2():  # Each level of hitter plays specific level of pitcher and returns full outcome breakdown
    for p in range(11):
        testing = pandas.DataFrame(columns=['K', 'BB', 'HR', 'S', 'D', 'T', 'IPHR', 'Outs', 'OPS', 'BABIP'])
        for i in range(11):
            testing.loc[len(testing)] = test2(i, p)
        print('hitter is row, pitcher is', p)
        print(testing)


def bigtest3():
    for p in range(11):
        testing = pandas.DataFrame(columns=['In-Swing', 'In-Take', 'Out-Swing', 'Out-Take', 'Pitch1', 'Pitch2', 'Pitch3'])
        for i in range(11):
            testing.loc[len(testing)] = test3(i, p)
        print('hitter is row, pitcher is', p)
        print(testing)


def bigtest4H():
    testing = pandas.DataFrame(columns=['Con', 'Pow', 'Vis', 'Speed', 'CP', 'CV', 'PV', 'ALL'])
    pitchers = [(0, 0, 0), (5, 5, 5), (10, 10, 10)]
    for i in range(11):
        hitters = [(i, 5, 5, 5), (5, i, 5, 5), (5, 5, i, 5), (5, 5, 5, i), (i, i, 5, 5), (i, 5, i, 5), (5, i, i, 5), (i, i, i, i)]
        testing.loc[i] = [test4(j, pitchers[0]) for j in hitters]
    print(testing)


def bigtest4P():
    testing = pandas.DataFrame(columns=['Cont', 'Velo', 'Move', 'CV', 'CM', 'VM', 'ALL'])
    hitters = [(0, 0, 0, 0), (5, 5, 5, 5), (10, 10, 10, 10)]
    for i in range(11):
        print(i)
        pitchers = [(i, 5, 5), (5, i, 5), (5, 5, i), (i, i, 5), (i, 5, i), (5, i, i), (i, i, i)]
        testing.loc[i] = [test4(hitters[0], j) for j in pitchers]
    print(testing)


def bigtest5():
    testing = pandas.DataFrame(columns=['pType', 'K', 'BB', 'HR', 'S', 'D', 'T', 'IPHR', 'Outs', 'OPS', 'BABIP'])
    for i in list(pitches.keys()):
        testing.loc[len(testing)] = test5(i)
    testing.set_index('pType', drop=True, inplace=True)
    print(testing)


def bigtest6():  # Each level of hitter plays specific level of pitcher and returns full outcome breakdown
    testing = pandas.DataFrame(columns=['K', 'BB', 'HR', 'S', 'D', 'T', 'IPHR', 'Outs', 'OPS', 'BABIP'])
    for i in range(11):
        testing.loc[len(testing)] = test6(i)
    print('hitter is 5, pitcher is 5, fielding is row')
    print(testing)


def bigWR():
    resDict = {'K': 8, 'BB': 5, 'Home Run': 4, 'single': 1, 'double': 2, 'triple': 3, 'IPHR': 4, 'SF': 7, 'out': 8,
               'FC': 8, 'DP': 6, 'LO': 8, 'FO': 8, 'GO': 8, 'Pop Out': 8, 'Foul Out': 8}
    weights = pandas.DataFrame(columns=['PA', 'S', 'D', 'T', 'HR', 'BB', 'DP', 'SF', 'OUT', 'RUNS'])
    bases = pandas.DataFrame(columns=['OUTS', '', '1', '2', '3', '12', '23', '13', '123'])
    basesAtt = pandas.DataFrame(columns=['OUTS', '', '1', '2', '3', '12', '23', '13', '123'])
    for i in range(3):
        bases.loc[i] = [i, 0, 0, 0, 0, 0, 0, 0, 0]
        basesAtt.loc[i] = [i, 0, 0, 0, 0, 0, 0, 0, 0]
    for hScore in range(11):
        print(hScore)
        hScore = 5
        for pScore in range(11):
            pScore = 5
            for fScore in range(11):
                fScore = 5
                board = Scoreboard('STL', 0)  # Busch Field is just like a fairly average park
                hitter = Hitter(nameGen(), 'H ')
                (hitter.con, hitter.pow, hitter.vis, hitter.field, hitter.speed) = (hScore, hScore, hScore, hScore, hScore)
                oLineup = Lineup(None, None, None)
                oLineup.dAlign = [hitter] * 10
                for j in range(9):
                    oLineup.battingOrder.loc[len(oLineup.battingOrder)] = [hitter, 'H ', hScore * 3, hitter.OPS]
                # Defense
                pitcher = Pitcher(nameGen(), 'P ', test=True)
                pitcher.stamScore = 99999999999999
                (pitcher.cont, pitcher.velo, pitcher.move, pitcher.field, pitcher.speed) = (pScore, pScore, pScore, fScore, fScore)
                dlineup = Lineup(None, None, None)
                dlineup.dAlign = [pitcher] * 10
                smallRes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                for j in range(100):
                    (runs, basesReached, PAres) = inning(oLineup, dlineup, 'h', board, 0, xrTest=True)
                    smallRes[9] += runs
                    for k in basesReached:
                        bases.loc[k[0], k[1]] += runs - k[2]
                        basesAtt.loc[k[0], k[1]] += 1
                    for k in PAres:
                        smallRes[0] += 1
                        smallRes[resDict[k]] += 1
                for spot in range(1, 10):
                    smallRes[spot] = round(smallRes[spot]/smallRes[0], 2)
                weights.loc[len(weights)] = smallRes
    basesFinal = pandas.DataFrame(columns=['OUTS', '___', '1__', '_2_', '__3', '12_', '_23', '1_3', '123'])
    for i in range(3):
        basesFinal.loc[i] = [i, 0, 0, 0, 0, 0, 0, 0, 0]
        for j in range(1, 9):
            basesFinal.iloc[i, j] = round(bases.iloc[i, j] / basesAtt.iloc[i, j], 2)
    basesFinal.set_index('OUTS', drop=True, inplace=True)
    with pandas.ExcelWriter('weightedRuns.xlsx') as writer:
        weights.to_excel(writer, sheet_name='PA Results')
        basesFinal.to_excel(writer, sheet_name='Bases')


def test(hScore, pScore):  # Sims a bunch of innings and returns a stat like ERA or OPS (currently ERA)
    # Offense
    board = Scoreboard('STL', 0)  # Busch Field is just like a fairly average park
    hitter = Hitter(nameGen(), 'H ')
    (hitter.con, hitter.pow, hitter.vis, hitter.field, hitter.speed) = (hScore, hScore, hScore, hScore, hScore)
    oLineup = Lineup(None, None, None)
    oLineup.dAlign = [hitter]*10
    for i in range(9):
        oLineup.battingOrder.loc[len(oLineup.battingOrder)] = [hitter, 'H ', hScore*3, hitter.OPS]
    # Defense
    pitcher = Pitcher(nameGen(), 'P ', test=True)
    (pitcher.cont, pitcher.velo, pitcher.move, pitcher.field, pitcher.speed) = (pScore, pScore, pScore, 5, 5)
    dlineup = Lineup(None, None, None)
    dlineup.dAlign = [pitcher] * 10
    for i in range(1000):
        if i%100 == 0 and i>0:
            #print(i)
            pass
        #print('new inning')
        dlineup.dAlign[1].stamScore = 1000
        inning(oLineup, dlineup, 'h', board, 6)
    hitter.calcStats()
    pitcher.calcStats()
    #print('Hitter:', hScore, 'Pitcher:', pScore)
    #print(hitter.PA, hitter.slash, hitter.OPS, hitter.HR, hitter.Sp)
    #print(pitcher.BF, pitcher.IP, pitcher.ERA, pitcher.WHIP, pitcher.Kp)
    return hitter.OPS


def test2(hScore, pScore):  # Sims a bunch of PAs and returns breakdown of results
    # Offense
    board = Scoreboard('STL', 0)
    hitter = Hitter(nameGen(), 'H ')
    (hitter.con, hitter.pow, hitter.vis, hitter.field, hitter.speed) = (hScore, hScore, hScore, hScore, hScore)
    oLineup = Lineup(None, None, None)
    oLineup.dAlign = [hitter] * 10
    for i in range(9):
        oLineup.battingOrder.loc[len(oLineup.battingOrder)] = [hitter, 'H ', hScore * 3, hitter.OPS]
    # Defense
    pitcher = Pitcher(nameGen(), 'P ', test=True)
    (pitcher.cont, pitcher.velo, pitcher.move, pitcher.field, pitcher.speed) = (pScore, pScore, pScore, 5, 5)
    dlineup = Lineup(None, None, None)
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
        res = PA(dlineup.dAlign, hitter, board)
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
        elif res[1] in ['out', 'FC', 'DP', 'LO', 'FO', 'GO', 'Pop Out', 'Foul Out']:
            outs += 1
        else:
            print(res, 'bruh')
    AVG = (HR+S+D+T+IPHR) / (10000 - BB)
    OBP = (HR+S+D+T+IPHR+BB) / 10000
    SLG = ((4*HR)+S+(2*D)+(3*T)+(4*IPHR)) / (10000 - BB)
    BABIP = (S+D+T+IPHR) / (10000 - BB - K - HR)
    return [int(K), int(BB), int(HR), int(S), int(D), int(T), int(IPHR), int(outs), int((OBP + SLG) * 1000), int(BABIP * 1000)]


def test3(hScore, pScore):  # Sims Pitches
    # Offense
    board = Scoreboard('STL', 0)
    hitter = Hitter(nameGen(), 'H ')
    (hitter.con, hitter.pow, hitter.vis, hitter.field, hitter.speed) = (hScore, hScore, hScore, hScore, hScore)
    oLineup = Lineup(None, None, None)
    oLineup.dAlign = [hitter] * 10
    for i in range(9):
        oLineup.battingOrder.loc[len(oLineup.battingOrder)] = [hitter, 'H ', hScore * 3, hitter.OPS]
    # Defense
    pitcher = Pitcher(nameGen(), 'P ', test=True)
    (pitcher.cont, pitcher.velo, pitcher.move, pitcher.field, pitcher.speed) = (pScore, pScore, pScore, pScore, pScore)
    dlineup = Lineup(None, None, None)
    dlineup.dAlign = [pitcher] * 10
    IS = 0
    IN = 0
    OS = 0
    ON = 0
    for i in range(10000):
        board.refresh()
        board.pitcher = pitcher
        board.hitter = hitter
        hitter.chargedTo = pitcher
        (zone, swing) = pitch(pitcher, hitter, board, dlineup.dAlign, False, test3=True)
        if zone and swing:
            IS += 1
        elif zone and not swing:
            IN += 1
        elif not zone and swing:
            OS += 1
        elif not zone and not swing:
            ON += 1
        else:
            print('uh ohhhhhhhhh')
    return [IS, IN, OS, ON, pitcher.arsenal[0], pitcher.arsenal[1], pitcher.arsenal[2]]


def test4(hScore, pScore):  # Sims a bunch of innings and returns a stat like ERA or OPS (currently ERA)
    # Offense
    board = Scoreboard('STL', 0)  # Busch Field is just like a fairly average park
    hitter = Hitter(nameGen(), 'H ')
    (hitter.con, hitter.pow, hitter.vis, hitter.speed) = hScore
    hitter.field = 5
    oLineup = Lineup(None, None, None)
    oLineup.dAlign = [hitter]*10
    for i in range(9):
        oLineup.battingOrder.loc[len(oLineup.battingOrder)] = [hitter, 'H ', hScore*3, hitter.OPS]
    # Defense
    pitcher = Pitcher(nameGen(), 'P ', test=True)
    (pitcher.cont, pitcher.velo, pitcher.move) = pScore
    (pitcher.field, pitcher.speed) = (5, 5)
    dlineup = Lineup(None, None, None)
    dlineup.dAlign = [pitcher] * 10
    for i in range(1000):
        if i%100 == 0 and i>0:
            #print(i)
            pass
        #print('new inning')
        dlineup.dAlign[1].stamScore = 1000
        inning(oLineup, dlineup, 'h', board, 0)
    hitter.calcStats()
    pitcher.calcStats()
    #print('Hitter:', hScore, 'Pitcher:', pScore)
    #print(hitter.PA, hitter.slash, hitter.OPS, hitter.HR, hitter.Sp)
    #print(pitcher.BF, pitcher.IP, pitcher.ERA, pitcher.WHIP, pitcher.Kp)
    return hitter.OPS


def test5(pType):  # Sims a bunch of PAs and returns breakdown of results
    # Offense
    board = Scoreboard('STL', 0)
    hitter = Hitter(nameGen(), 'H ')
    (hitter.con, hitter.pow, hitter.vis, hitter.field, hitter.speed) = (5, 5, 5, 5, 5)
    oLineup = Lineup(None, None, None)
    oLineup.dAlign = [hitter] * 10
    for i in range(9):
        oLineup.battingOrder.loc[len(oLineup.battingOrder)] = [hitter, 'H ', 15, hitter.OPS]
    # Defense
    pitcher = Pitcher(nameGen(), 'P ', test=True)
    (pitcher.cont, pitcher.velo, pitcher.move, pitcher.field, pitcher.speed) = (5, 5, 5, 5, 5)
    pitcher.arsenal = [pType]
    dlineup = Lineup(None, None, None)
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
        res = PA(dlineup.dAlign, hitter, board)
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
        elif res[1] in ['out', 'FC', 'DP', 'LO', 'FO', 'GO', 'Pop Out', 'Foul Out']:
            outs += 1
        else:
            print(res, 'bruh')
    AVG = (HR+S+D+T+IPHR) / (10000 - BB)
    OBP = (HR+S+D+T+IPHR+BB) / 10000
    SLG = ((4*HR)+S+(2*D)+(3*T)+(4*IPHR)) / (10000 - BB)
    BABIP = (S+D+T+IPHR) / (10000 - BB - K - HR)
    return [pType, int(K), int(BB), int(HR), int(S), int(D), int(T), int(IPHR), int(outs), int((OBP + SLG) * 1000), int(BABIP * 1000)]


def test6(fScore):
    # Offense
    board = Scoreboard('STL', 0)
    hitter = Hitter(nameGen(), 'H ')
    #(hitter.con, hitter.pow, hitter.vis, hitter.field, hitter.speed) = (5, 5, 5, 5, 5)
    (hitter.con, hitter.pow, hitter.vis, hitter.field, hitter.speed) = (10, 10, 10, 10, 10)
    oLineup = Lineup(None, None, None)
    oLineup.dAlign = [hitter] * 10
    for i in range(9):
        oLineup.battingOrder.loc[len(oLineup.battingOrder)] = [hitter, 'H ', 5 * 3, hitter.OPS]
    # Defense
    pitcher = Pitcher(nameGen(), 'P ', test=True)
    (pitcher.cont, pitcher.velo, pitcher.move, pitcher.field, pitcher.speed) = (0, 0, 0, fScore, fScore)
    dlineup = Lineup(None, None, None)
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
        res = PA(dlineup.dAlign, hitter, board)
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
        elif res[1] in ['out', 'FC', 'DP', 'LO', 'FO', 'GO', 'Pop Out', 'Foul Out']:
            outs += 1
        else:
            print(res, 'bruh')
    AVG = (HR + S + D + T + IPHR) / (10000 - BB)
    OBP = (HR + S + D + T + IPHR + BB) / 10000
    SLG = ((4 * HR) + S + (2 * D) + (3 * T) + (4 * IPHR)) / (10000 - BB)
    BABIP = (S + D + T + IPHR) / (10000 - BB - K - HR)
    return [int(K), int(BB), int(HR), int(S), int(D), int(T), int(IPHR), int(outs), int((OBP + SLG) * 1000),
            int(BABIP * 1000)]
