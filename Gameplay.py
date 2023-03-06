from DirectoryWide import *
from Linked_List3 import *
from inputimeout import inputimeout
import datetime
import time
import random
import math
import numpy
import pandas

# P-Value (printout for a game) Keys:
# 0 Nothing
# 1 Scoreboard
# 2 PA results
# 3 adds fielding and baserunning
# 4 Pitch-by-Pitch
testerDF = pandas.DataFrame(columns=['CScore', 'Power', 'Result'])


class Scoreboard:  # Like the sheet from curling, carries everything from function that you need.
    def __init__(self, stadium, p):
        self.stadium = stadiums[stadium]  # How many times can I write 'stadium' in one line?. Stadiums from DirWide
        self.inning = 1
        self.hOrder = 0  # Tracks where in the batting order the home team is.
        self.aOrder = 0
        self.hitter = None  # PA to PA... I'm pretty sure it's for stats
        self.pitcher = None  # same
        self.strikes = 0
        self.balls = 0
        self.outs = 0
        self.B1 = None  # Who is "on" each base. Generally* it's the last base you touched if in motion.
        self.B2 = None  # *Except fast forward but we'll get there when we get there
        self.B3 = None
        self.basepaths = [0, 0, 0, 0]  # How far along each baseline a runner is.
        # ^ first is hitter distance past home. Second is B1 past first base. So on
        self.force = True  # If force play is on, implicated people have to run.
        self.scoring = 'out'  # Baseline, if the result is anything else we'll change it later.
        self.user = None
        self.p = p
        self.permP = p

    def refresh(self):  # New inning
        self.strikes = 0
        self.balls = 0
        self.outs = 0
        self.B1 = None
        self.B2 = None
        self.B3 = None
        self.basepaths = [0, 0, 0, 0]
        self.force = True
        self.scoring = 'out'
        self.p = self.permP

    def newPA(self, hit, pitch):  # New P... oh it's right in the name (#comedy)
        self.hitter = hit
        self.pitcher = pitch
        self.strikes = 0
        self.balls = 0
        self.force = True
        self.scoring = 'out'

    def clearBases(self):
        self.B1 = None
        self.B2 = None
        self.B3 = None

    def showRunners(self):
        print(self.hitter, self.B1, self.B2, self.B3)
        print(self.basepaths)

    def showRunnersSmall(self):
        print(self.hitter, self.B1, self.B2, self.B3)

    def count(self):
        return str(self.balls) + '-' + str(self.strikes)


def findVinit(accel, disp, time):  # KINEEEEEEMATIC EQUATIONS
    return (disp - .5*accel*(time**2)) / time


def findVfinal(accel, velo, time):
    return accel*time + velo


def findP(accel, velo, pos, time):
    return .5*accel*(time**2) + velo*time + pos


def findT(accel, velo, pF, pI):  # This is +- in there but I used - cuz it's the later (real) one
    if velo**2 - 2*accel*(pI - pF) <= 0:
        print('nonononon')
    return (-velo - math.sqrt(velo**2 - 2*accel*(pI - pF))) / accel


def game(home, away, playoff=False, p=0, stam=SPstam):  # p is a print value that informs output, stam input is for ASG
    board = Scoreboard(home.ABR, p)  # Plays game with home team's walls
    home.setLineup()  # Roster rotation, builds strong roster using available players
    away.setLineup()  # I'm not going to advertise best possible, but a good one.
    hlineup = home.lineupCard  # From here in you can read 'hlineup' as 'home team'
    alineup = away.lineupCard
    if home.controlled or away.controlled:
        board.permP = max(board.p, 1)
    if alineup.containsControlled():
        board.user = alineup.containsControlled()
        board.permP = max(board.p, 2)
    elif hlineup.containsControlled():
        board.user = hlineup.containsControlled()
        board.permP = max(board.p, 2)
    board.p = board.permP
    if board.p >= 2:  # When showing every PA, I like to know the players positions and stuff, plus i think it's cool
        print(home.name, 'lineup')
        hlineup.printout()
        print(away.name, 'lineup')
        alineup.printout()
    aF = 0  # Overall Score
    hF = 0
    hlineup.dAlign[1].stamScore = stam  # dAlign[1] is the pitcher, specifically the Starting Pitcher.
    alineup.dAlign[1].stamScore = stam
    aScore = Linked_List()  # Each inning score will go in here
    hScore = Linked_List()  # These are used just for the scoreboard at the end
    inns = Linked_List()  # Just the inning number
    while board.inning <= 9 or aF == hF:  # You should see how I used to do this.
        if board.p >= 2:
            print('TOP', board.inning, away.ABR, 'is hitting.', away.ABR, str(aF)+'-'+str(hF), home.ABR)
        inns.append(board.inning)
        aE = inning(alineup, hlineup, 'a', board)  # Returns the score from that inning. Future might also include hits
        aScore.append(aE)
        aF += aE
        if board.p >= 2:
            print('BOT', board.inning, home.ABR, 'is hitting.', away.ABR, str(aF)+'-'+str(hF), home.ABR)
        if board.inning >= 9 and hF > aF:  # Game ends early
            hE = 'x'
            if board.p >= 2:
                print('BOT', board.inning, 'is irrelevant')
        elif board.inning < 9:
            hE = inning(hlineup, alineup, 'h', board)
        else:  # Bottom 9 with home team not winning already means walkoff is in play.
            hE = inning(hlineup, alineup, 'h', board, wOff=aF-hF)
        hScore.append(hE)
        if isinstance(hE, int):  # bc it might be 'x' and that'll just blow everything up
            hF += hE
        board.inning += 1
    if board.p >= 1:  # This is the scoreboard
        print('Name                 ' + str(inns) + '||F')
        print('------------------------' + '--' * board.inning)
        print(away.name + str(aScore) + '||' + str(aF))
        print('------------------------' + '--' * board.inning)
        print(home.name + str(hScore) + '||' + str(hF))
    # Post-Game
    hlineup.statsUP()  # Updates stats of all hitters and pitchers
    alineup.statsUP()
    hlineup.usage()  # Designates who needs a rest day in the next game.
    alineup.usage()
    if not playoff:  # Regular season game
        home.played += 1
        away.played += 1
        home.runsFor += hF
        home.runsAgainst += aF
        away.runsFor += aF
        away.runsAgainst += hF
        if hF > aF:
            home.wins += 1
            if home.streak < 0:
                home.streak = 1
            else:
                home.streak += 1
            if away.streak > 0:
                away.streak = -1
            else:
                away.streak -= 1
        else:
            away.wins += 1
            if away.streak < 0:
                away.streak = 1
            else:
                away.streak += 1
            if home.streak > 0:
                home.streak = -1
            else:
                home.streak -= 1
        if board.p >= 1:
            print(home.ABR, home.record(), away.ABR, away.record())
        if home.streak >= 10:
            print(home, home.record(), 'have won', home.streak, 'games in a row!')
        elif home.streak <= -10:
            print(home, home.record(), 'have lost', -1 * home.streak, 'games in a row!')
        if away.streak >= 10:
            print(away, away.record(), 'have won', away.streak, 'games in a row!')
        elif away.streak <= -10:
            print(away, away.record(), 'have lost', -1 * away.streak, 'games in a row!')
    else:
        if hF > aF:
            home.pWins += 1
        else:
            away.pWins += 1


def inning(oTeam, dTeam, side, board, wOff=10000):  # Yes technically innings have a mercy cap of 10000
    board.refresh()
    if board.user == dTeam.dAlign[1]:
        board.p = 4
    elif board.user in dTeam.dAlign:
        board.p = 3
    offense = oTeam.battingOrder
    runs = 0
    while board.outs < 3 and runs <= wOff:
        order = board.hOrder if side == 'h' else board.aOrder
        hitter = offense['Name'].iloc[order]
        if board.user == hitter:
            board.p = 4
            board.showRunners()
            print(board.outs)
        hitter.PA += 1
        if dTeam.dAlign[1].stamScore < 0:
            changePitcher(dTeam, board)
        pitcher = dTeam.dAlign[1]
        hitter.chargedTo = pitcher  # This is for pitcher ERA bc its not who let them score its who put them on base
        pitcher.BF += 1
        if board.p >= 4:
            print(pitcher, 'is pitching', dTeam.dAlign[1].stamScore)
        board.newPA(hitter, pitcher)
        res = PA(dTeam.dAlign, hitter, board)
        if res == 'K':  # 3 true outcomes get their own results
            pitcher.K += 1
            pitcher.OR += 1  # Outs Recorded
            hitter.K += 1
            board.outs += 1
            dTeam.dAlign[1].stamScore += 2  # pitchers doing well will stay out longer given pitch count
        elif res == 'BB':
            pitcher.BB += 1
            hitter.BB += 1
            dTeam.dAlign[1].stamScore -= 1
            if board.B1:
                if board.B2:  # Baserunners only move up if forced
                    if board.B3:
                        hitter.RBI += 1
                        board.B3.R += 1
                        board.B3.chargedTo.ER += 1
                        runs += 1
                    board.B3 = board.B2
                board.B2 = board.B1
            board.B1 = hitter
        elif res == 'Home Run':
            hitter.H += 1
            hitter.HR += 1
            hitter.TB += 4
            hitter.RBI += 1
            hitter.R += 1
            pitcher.H += 1
            pitcher.HR += 1
            hitter.chargedTo.ER += 1
            dTeam.dAlign[1].stamScore -= 8
            runs += 1
            if board.B1:
                hitter.RBI += 1
                board.B1.R += 1
                board.B1.chargedTo.ER += 1
                runs += 1
            if board.B2:
                hitter.RBI += 1
                board.B2.R += 1
                board.B2.chargedTo.ER += 1
                runs += 1
            if board.B3:
                hitter.RBI += 1
                board.B3.R += 1
                board.B3.chargedTo.ER += 1
                runs += 1
            board.clearBases()
        elif isinstance(res, list):  # Ball in play returns [runs, scoring]
            runs += res[0]
            hitter.RBI += res[0]
            if res[1] not in ['out', 'FC', 'DP']:  # It was a hit.
                dTeam.dAlign[1].stamScore -= 2
                statsHelp(res[1], hitter, pitcher)  # all the hits and TB for balls in play
        if board.user == hitter:
            board.p = 3
        if side == 'h':
            board.hOrder = (board.hOrder + 1) % 9  # Mod so it just starts back at top of the order
        else:
            board.aOrder = (board.aOrder + 1) % 9
        if board.p >= 2:  # Print result of the PA
            if isinstance(res, list):
                print(dTeam.dAlign[1].smallLine(), 'v', hitter.smallLine(), res[1], runs)
            else:
                print(dTeam.dAlign[1].smallLine(), 'v', hitter.smallLine(), res, runs)
        if board.p >= 3:  # Shows the bases
            board.showRunnersSmall()
    return runs


def PA(defense, hitter, board):
    pitcher = defense[1]
    while board.balls < 4 and board.strikes < 3:
        if board.p >= 4:
            print(board.count())
        steal = stealDec(board)  # Decides if runner goes, returns a boolean
        if steal and board.p >= 3:
            print('Runner goes!')
        res = pitch(pitcher, hitter, board, defense, steal)
        pitcher.stamScore -= 1
        if res == 'strike':
            board.strikes += 1
        elif res == 'ball':
            board.balls += 1
        elif res == 'foul ball':
            if board.strikes < 2:
                board.strikes += 1
        elif res == 'whiff':  # I mean it's just a strike but it gets called from a different place and maybe stats
            board.strikes += 1
        else:
            return res  # kills the PA there
    if board.balls == 4:
        return 'BB'
    if board.strikes == 3:
        return 'K'


def pitch(pitcher, hitter, board, defense, steal, test3=False):  # This is the nitty-gritty
    # Pitch Selection
    if pitcher.controlled:
        print(pitcher.arsenal)
        try:
            choice = int(input('Which pitch do you want to throw, first is 0, second is 1, etc.'))
            pType = pitcher.arsenal[choice]
        except ValueError or IndexError:  # If user messes up, so the entire thing doesnt come crashing down
            pType = random.choice(pitcher.arsenal)
    else:
        pType = random.choice(pitcher.arsenal)
    # print(pType)
    #pType = 'SPLT'
    baselines = pitches[pType]
    Ax = baselines[0] * (.7 + .06 * (pitcher.move - 1))  # Higher movement pitchers get more acceleration
    Ay = (baselines[1] * (.7 + .06 * (pitcher.move - 2))) + gravForce
    Az = 0  # For now, no drag
    Vz = -1 * (baselines[2] + (1 * (pitcher.velo - 5) * mphTOfts))
    Px = pitcher.release[0]  # Starting spot
    Py = pitcher.release[1]
    distToPlate = rubberToPlate - pitcher.extension
    Pz = rubberToPlate - pitcher.extension  # This one can change, while distToPlate will remain constant
    timeToPlate = - Pz / Vz  # constant velo
    if steal:  # how far they got during the pitch
        board.basepaths[1] = (20 + .5 * board.B1.speed) * (timeToPlate + .9)
    timeTraveled = 0
    if pitcher.controlled:
        xPick = float(input('X-coordinate aim?'))
        yPick = float(input('Y-coordinate aim?'))
        pAtt = [xPick, yPick]
    else:
        # pAtt = [baselines[3], baselines[4]]  # Standard spot for given pitch type
        # pAtt = [0, 2.5]
        pAtt = [random.uniform(-1.2, 1.2), random.uniform(1, 4)]
    pSpot = [numpy.random.normal(pAtt[0], max((17-pitcher.cont)*.02, 0)), numpy.random.normal(pAtt[1], max((17-pitcher.cont)*.04, 0))]
    #print(pSpot)
    Vx = numpy.random.normal(findVinit(Ax, pSpot[0] - Px, timeToPlate), 0)  # The normal doesnt do anything rn
    Vy = numpy.random.normal(findVinit(Ay, pSpot[1] - Py, timeToPlate), 0)  # Used to, kept in case i want it back
    # print(round(Ax, 2), round(Ay, 2), round(Vx, 2), round(Vy, 2), round(Vz, 2))
    Xs = []
    Ys = []
    Zs = []
    PzCopy = Pz
    crossPlate = [findP(Ax, Vx, Px, timeToPlate), findP(Ay, Vy, Py, timeToPlate)]  # X and Y coordinates at Pz=0
    if hitter.controlled:
        while PzCopy > -7:  # Sets up all the locations during the path so you dont have to have the system doing math
            Xs.append(numpy.random.normal(findP(Ax, Vx, Px, timeTraveled), .5 - (.05 * hitter.vis)))
            Ys.append(numpy.random.normal(findP(Ay, Vy, Py, timeTraveled), .5 - (.05 * hitter.vis)))
            PzCopy = numpy.random.normal(findP(Az, Vz, Pz, timeTraveled), .5 - (.05 * hitter.vis))
            Zs.append(PzCopy)
            timeTraveled += split  # can change split for more loc points
        swing = None  # if no button is pressed it defaults to no swing
        i = 0
        if steal:
            print('Runner Goes!')
        dud = input('pitch is coming now')  # User has to hit enter to start pitch
        time = 0
        while swing is None and i < len(Xs):
            try:
                start_time = datetime.datetime.now()
                swing = inputimeout(str(round(Xs[i], 2))+' '+str(round(Ys[i], 2))+' '+str(round(Zs[i], 2)), timeout=.05)
                # Will almost definitely be '' which is technically False but also not None so its cool
                final_time = datetime.datetime.now()
                inputTime = final_time - start_time
                toAdd = inputTime.microseconds / 1000000  # this is just how you have to do it man idk
                timeTotal = time + (toAdd / (.05 / split))
                xSwing = findP(Ax, Vx, Px, timeTotal)
                ySwing = findP(Ay, Vy, Py, timeTotal)
                zSwing = findP(Az, Vz, Pz, timeTotal)
                penalty = .1 * (10 - hitter.vis)
            except Exception:  # Basically keeps the while loop going, terrible coding practice never do this
                i += 1
                time += split
                continue  # Sometimes you just need a continue that doesn't do anything
    else:
        if steal and board.strikes != 2:
            swing = None  # Swinging when the runner goes is generally frowned upon
        else:  # TAKE 2, it didn't really work but what can ya do
            swing = None
            #decDist = 20
            #decTime = (distToPlate - decDist) / -Vz  # When they have to make a decision
            decTime = timeToPlate - .25
            # for all of this, t at the end means true, g means guess.
            (xPt, yPt, zPt) = (findP(Ax, Vx, Px, decTime), findP(Ay, Vy, Py, decTime), findP(Az, Vz, Pz, decTime))
            (xVt, yVt, zVt) = (findVfinal(Ax, Vx, decTime), findVfinal(Ay, Vy, decTime), findVfinal(Az, Vz, decTime))
            xPg = numpy.random.normal(xPt, max((.01 * (10-hitter.vis) + .01 * pitcher.velo), 0))
            yPg = numpy.random.normal(yPt, max((.01 * (10-hitter.vis) + .01 * pitcher.velo), 0))
            zPg = numpy.random.normal(zPt, max((.1 * (10-hitter.vis) + .1 * pitcher.velo), 0))
            xVg = numpy.random.normal(xVt, max((.1 * (10-hitter.vis) + .1 * pitcher.velo), 0))
            yVg = numpy.random.normal(yVt, max(.1 * (10-hitter.vis) + .1 * pitcher.velo, 0))
            zVg = (distToPlate - zPg)/decTime
            timeLeftG = zPg / zVg
            cpG = [findP(0, xVg, xPg, timeLeftG), findP(gravForce, yVg, yPg, timeLeftG)]  #
            if -.875 <= cpG[0] <= .875 and 1.5 <= cpG[1] <= 3.5:  # If they think it's in the zone
                swing = ''
                penalty = 4 * pythag(cpG[0] - crossPlate[0], cpG[1]-crossPlate[1])
                swingTime = decTime + timeLeftG
                xSwing = findP(Ax, Vx, Px, swingTime)
                ySwing = findP(Ay, Vy, Py, swingTime)
                zSwing = findP(Az, Vz, Pz, swingTime)
                hitter.swings += 1
                hitter.zMissT += abs(zSwing)
    if test3:
        zone = (-.875 <= crossPlate[0] <= .875) and (1.5 <= crossPlate[1] <= 3.5)
        if swing is None:
            whoop = False
        else:
            whoop = True
        return (zone, whoop)
    # TAKE 1, instead of guessing P and V values, take 1 allowed higher vision players to make decisions later
        # So they could see more of the break
    """  # Tab it out once if you want to use it
    else:
        swing = None
        decTime = clamp(timeToPlate - (.4 - .03 * hitter.vis), 0, timeToPlate)
        xDec = findP(Ax, Vx, Px, decTime)
        yDec = findP(Ay, Vy, Py, decTime)
        zDec = findP(Az, Vz, Pz, decTime)
        timeLeft = timeToPlate - decTime
        yAdj = findP(gravForce, Ay*decTime + Vy, 0, timeLeft)
        xAdj = findP(0, Ax*decTime + Vx, 0, timeLeft)
        # print(xDec, xDec + xAdj, yDec, yDec + yAdj, zDec)
        if -.875 <= xDec + xAdj <= .875 and 1.5 <= yDec + yAdj <= 3.5:
            swing = ''
            hitter.swings += 1
            swingTime = numpy.random.normal(.428, .03)  # .428 is 86 mph and 6.5 ft extension
            if timeToPlate > swingTime:  # Swingin early
                adjust = (.75 - .05*hitter.con) * (timeToPlate - swingTime)
                swingTime = timeToPlate - adjust
            elif timeToPlate < swingTime:
                adjust = (.75 - .05 * hitter.con) * (swingTime - timeToPlate)
                swingTime = timeToPlate + adjust
            xSwing = findP(Ax, Vx, Px, swingTime)
            ySwing = findP(Ay, Vy, Py, swingTime)
            zSwing = findP(Az, Vz, Pz, swingTime)
            hitter.zMissT += abs(zSwing)
    """
    if swing is None:  # Swing Adjudication starts here. This is pitch taken
        if hitter.controlled:
            dud = input('Just hit enter, here to catch a late swing')
        if steal:
            spiked = crossPlate[0] < .5  # Much harder for the catcher to get a clean throw off
            stealAdj(board, defense[2], spiked)  # defender 2 is the catcher
        if board.p >= 4:
            print(pType, crossPlate)
        if -.875 <= crossPlate[0] <= .875 and 1.5 <= crossPlate[1] <= 3.5:  # In the strike zone
            if board.p >= 4:
                print('called strike')
            return 'strike'
        else:
            if board.p >= 4:
                print('ball')
            return 'ball'
    else:  # This is the engine room, not sure if it really makes any sense
        offCenter = pythag(xSwing/.875, ySwing - 2.5)  # Edge of the K zone returns 1.
        contactScore = (13 - (zSwing**2)) * (1.1 - math.sin(min(offCenter, 2) * math.pi * .25)) * math.sqrt(1.1 + hitter.con*.01)
        # quad is so 10-hitter gets x2, 0 hitter gets x.5.
        # Sin so oC of 1 gets you like x.3, dead center is x1, oC of 2 or more goes to 0.
        if hitter.hand * pitcher.hand == -1:  # Wanted some kind of benefit for this, but I dont really get it
            contactScore += 1
        contactScore -= penalty
        if board.p >= 4:
            print('Z:', round(zSwing, 2), 'Off-center:', round(offCenter, 2), 'cScore:', round(contactScore, 2))
        if contactScore < 1 or ySwing <= 0:  # So bad of contact there wasn't even contact
            if steal:
                spiked = crossPlate[0] < .5
                stealAdj(board, defense[2],  spiked)
            return 'whiff'
        else:  # Bat on Ball action
            launchAngle = math.radians(numpy.random.normal(35, max(0, 10*(10-contactScore))))
            exitVelo = (4*contactScore + 20*(1.5 + hitter.pow*.02)) * mphTOfts
            angle = math.radians(numpy.random.uniform(-45, 135))  # This is direction, like to left field or right field
            # Right now this is pretty whack, so this is subject to change when I figure out a better way to get FBs^
            if board.p >= 3:
                print('Exit Velo:', round(exitVelo, 2), 'Launch Angle:', round(math.degrees(launchAngle), 2), 'Dir. Angle:', round(math.degrees(angle), 2))
            bip = ballInPlay(exitVelo*math.cos(launchAngle), exitVelo*math.sin(launchAngle), ySwing, angle, defense, board, steal)
            # if isinstance(bip, list):
                # testerDF.loc[len(testerDF)] = [contactScore, hitter.pow, bip[1]]
            # else:
                # testerDF.loc[len(testerDF)] = [contactScore, hitter.pow, bip]
            return bip
            # ^ Look okay, you need to know a lot


def ballInPlay(Vx, Vy, height, angle, defense, board, steal):
    # ball in play dimensions are different, Vy is up, Vx is away from plate, angle 0 is 1B line.
    foulBall = angle < 0 or angle > math.pi/2 or Vx < 0  # gosh i hate radians, last one is fouled back
    timeInAir = findT(gravForce, Vy, 0, height)
    distTraveled = Vx * timeInAir  # For now no drag, but I might add it so I can have "Coors!"
    wallSegment = clamp(int(angle // (math.pi/10)), 0, 4)
    wallDist = board.stadium[4 - wallSegment]
    if distTraveled > wallDist and not foulBall:  # Im gonna add a thing about needed to be like 8 feet high at the wall
        if board.p >= 4:
            print('Wall Distance', wallDist)
        return 'Home Run'
    if inSeatsFoul(distTraveled, angle, board.stadium):  # Need to check this before the catch, but regular foul after
        if steal:
            board.basepaths[1] = 0
        if board.p >= 3:
            print('foul ball')
        return 'foul ball'
    catch = catchCheck(timeInAir, defense, distTraveled, angle)  # Returns player object, which is a True value
    if catch:
        if board.p >= 3:
            print('ball is caught')
        if steal:  # Ya gotta go back
            board.basepaths[1] = 0
        board.outs += 1
        board.pitcher.OR += 1
        defense[1].stamScore += 1
        board.hitter = None
        board.force = False
        if steal:
            board.basepaths[1] = 0
        [time, dist, fielder] = [0, distTraveled, catch]  # Don't return right away bc people might tag up.
    if not catch and foulBall:
        if steal:
            board.basepaths[1] = 0
        if board.p >= 3:
            print('foul ball')
        return 'foul ball'
    elif not catch:
        if board.p >= 3:
            print('ball is down')
        [time, dist, fielder] = pickupBall(Vx, distTraveled, angle, defense, timeInAir, wallDist)  # angle constant
    if board.p >= 3:
        print(defense.index(fielder), fielder, 'has the ball at', dist, time)
    runs = 0
    newRuns = prePickupRunnin(board, time)  # For extra base hits, so hitter running to second is treated correctly
    runs += newRuns
    runners = baseRunDec(time, dist, angle, board)  # Returns list of who is running, the player objects
    while runners and board.outs < 3:
        throw = throwDec(fielder, defense, time, dist, angle, runners, board)  # Int of where the throw is going
        if board.p >= 4:
            print(*runners, 'are running')
            board.showRunners()
            print('throw is to', throw)
        [dist, angle, fielder, newRuns, time] = adjudication(fielder, dist, angle, runners, throw, board, time, defense)
        # Moves runners, safe or out calls, runs, and new checkpoint all in one
        if board.outs >= 3:
            if not board.force:  # If the inning ends and the force is still live then the runs dont score for that play
                runs += newRuns
            break  # End of play if you hit 3 outs
        runs += newRuns
        if board.p >= 3:
            print(defense.index(fielder), fielder, 'has the ball at', dist, time)
        if board.hitter is None:
            board.force = False
        runners = baseRunDec(time, dist, angle, board)  # Have to do it at the end bc if its empty that's the break
    return [runs, board.scoring]  # Shoots this back up the chain to the inning


def inSeatsFoul(dist, angle, stadium):  # Ball out of play, cannot be caught
    # Coordinate system is weird for this, 1B line is x axis, 3B line is y axis, Home plate is (0,0)
    coords = polarToCartesian(dist, angle)
    RFline = lineDef(stadium[0], 0)  # X, Y of second point, backstop built into the function
    LFline = lineDef(0, stadium[4])
    return coords[1] < RFline[0]*coords[0] + RFline[1] or coords[1] > LFline[0]*coords[0] + LFline[1]


def catchCheck(timeToGround, defense, dist, angle):
    spots = list(range(1, 10))  # Don't use 0 because its the DH and not in the field.
    closestToSpot(spots, dist, angle)
    for i in spots:  # Cycles through defenders in order of distance so the pitcher doesn't make every infield catch
        player = defense[i]
        startSpot = positions[posNotation[i]]  # [Dist, Angle] of the position
        distToCover = polarDistance(dist, startSpot[0], angle, startSpot[1])
        if player.canGetThere(distToCover, timeToGround):  # From Players.py
            return player
    return None  # False Value, signals that no catch was made because no one could get there


def closestToSpot(array, dist, angle):  # I think it's insertion sort I dunno i took it from g4g
    for s in range(len(array)):
        min_idx = s
        for i in range(s + 1, len(array)):
            if polarDistance(dist, positions[posNotation[array[i]]][0], angle, positions[posNotation[array[i]]][1])\
                    < polarDistance(dist, positions[posNotation[array[min_idx]]][0], angle, positions[posNotation[array[min_idx]]][1]):
                min_idx = i
        (array[s], array[min_idx]) = (array[min_idx], array[s])


def pickupBall(Vx, dist, angle, defense, startTime, wallDist):  # Has hit the ground, but otherwise sim to catchCheck
    timeSinceHit = 0
    spots = list(range(1, 10))
    while timeSinceHit < 1000000000:  # Just goes until returned
        ballPos = min(findP(frictionDecel, Vx, dist, timeSinceHit), wallDist)  # Currently no bouncing it just rolls
        closestToSpot(spots, ballPos, angle)
        #print(spots)
        for i in spots:
            player = defense[i]
            startSpot = positions[posNotation[i]]
            distToCover = polarDistance(dist, startSpot[0], angle, startSpot[1])
            if player.canGetThere(distToCover, startTime+timeSinceHit):
                return [startTime + timeSinceHit, ballPos, player]  # add rolling time to the checkpoint
        timeSinceHit += .1


def throwDec(fielder, defense, timeSinceCheckpoint, dist, angle, runners, board):  # Fielders pick where to throw.
    # fielder has the ball, defense is the whole team, dist is from plate as usual
    throwSpeed = (75 + fielder.field) * mphTOfts
    guessRunTimeH = (90-board.basepaths[3]) / 22.5  # Guesses assume average runner so bad decisions can be made
    guessRunTime3 = (90 - board.basepaths[2]) / 22.5
    guessRunTime2 = (90 - board.basepaths[1]) / 22.5
    guessRunTime1 = (90 - board.basepaths[0]) / 19.5
    distTo1st = polarDistance(dist, 90, angle, 0)
    distTo2nd = polarDistance(dist, 90*math.sqrt(2), angle, math.pi/4)
    distTo3rd = polarDistance(dist, 90, angle, math.pi/2)
    distToHome = dist
    timeThrow1st = .75 + (distTo1st / throwSpeed)
    timeThrow2nd = .75 + (distTo2nd / throwSpeed)
    timeThrow3rd = .75 + (distTo3rd / throwSpeed)
    timeThrowHome = .75 + (distToHome / throwSpeed)
    if fielder.controlled:  # Lets user controlled player decide where to throw
        print('Checkpoint Time, Throw time, Guess Run Time')
        allowed = [4, 5]
        if board.B3 in runners:  # In runners means they're running to next base
            allowed.append(0)
            print('To Home (0):', round(timeSinceCheckpoint, 2), round(timeThrowHome, 2), round(guessRunTimeH))
        if board.hitter in runners:
            allowed.append(1)
            print('To First (1):', round(timeSinceCheckpoint, 2), round(timeThrow1st, 2), round(guessRunTime1))
        if board.B1 in runners:
            allowed.append(2)
            print('To Second (2):', round(timeSinceCheckpoint, 2), round(timeThrow2nd, 2), round(guessRunTime2))
        if board.B2 in runners:
            allowed.append(3)
            print('To Third (3):', round(timeSinceCheckpoint, 2), round(timeThrow3rd, 2), round(guessRunTime3))
        print('4-No Throw(P)', '5-No Throw(2nd)')  # It do be making a difference actually
        try:
            choice = int(input('Where throw?'))
            if choice in allowed:  # Throws to bases trigger safe/out call, i think it might break if no one is there
                return choice
            else:
                return 4
        except ValueError:  # If they give a bad input, you dont want it to break the whole thing
            return 4
    if board.outs == 2:  # If you have 2 outs, take the out you're most confident in
        surpluses = [0]*4
        if board.B3 in runners:
            surpluses[0] = timeSinceCheckpoint + timeThrowHome - guessRunTimeH
        if board.hitter in runners:
            surpluses[1] = timeSinceCheckpoint + timeThrow1st - guessRunTime1
        if board.B1 in runners:
            surpluses[2] = timeSinceCheckpoint + timeThrow2nd - guessRunTime2
        if board.B2 in runners:
            surpluses[3] = timeSinceCheckpoint + timeThrow3rd - guessRunTime3
        if board.p >= 3:
            print(surpluses)
        if min(surpluses) < 0:
            return surpluses.index(min(surpluses))  # I like this little trick
        else:
            if defense.index(fielder) >= 7:  # Outfielders
                return 5
            else:
                return 4
    else:  # Non-2 outs, take the most advanced out you think you can get, facilitates double play.
        if board.B3 in runners and timeSinceCheckpoint+timeThrowHome < guessRunTimeH:
            return 0
        elif board.B2 in runners and timeSinceCheckpoint+timeThrow3rd < guessRunTime3:
            return 3
        elif board.B1 in runners and timeSinceCheckpoint + timeThrow2nd < guessRunTime2:
            return 2
        elif board.hitter in runners and timeSinceCheckpoint+timeThrow1st < guessRunTime1:
            return 1
        else:
            if defense.index(fielder) >= 7:
                return 5
            else:
                return 4


def baseRunDec(time, dist, angle, board):  # Runners decide whether to go. time here is Checkpoint time
    running = []  # This will eventually get returned, if still empty then, no one is running and play is dead
    guessThrowSpeed = 80 * mphTOfts  # Guess is for average fielder, so bad decisions can be made
    if board.B3:
        runTime = (90 - board.basepaths[3]) / (20 + .5 * board.B3.speed)
        if board.B2 and board.B1 and board.force:  # Bases loaded
            if board.B3.controlled:
                print('Force play, you are running to home')
            running.append(board.B3)
        else:
            guessThrowTime = .75 + (dist / guessThrowSpeed)
            if board.B3.controlled:
                print('Input anything to run to home, just hit enter to stay.')
                print('Checkpoint Time', round(time, 2), 'Run Time', round(runTime, 2), 'Estimated Throw Time', round(guessThrowTime, 2))
                choice = input('Run?')  # Since no int conversion, no need for try/except block
                if choice:  # Anything but empty input
                    running.append(board.B3)
                else:
                    board.basepaths[3] = 0  # Return to the bag if you are off
            else:  # Com dec making
                if runTime < guessThrowTime + time:
                    running.append(board.B3)
                else:
                    board.basepaths[3] = 0
    if board.B2:
        runTime = (90 - board.basepaths[2]) / (20 + .5 * board.B2.speed)
        if board.B1 and board.force:
            if board.B2.controlled:
                print('Force play, you are running to third')
            running.append(board.B2)
        elif board.B3 and board.B3 not in running:  # can be elif since if B3 and you caught the first if then B3 runs
            if board.B2.controlled:
                print('Runner Stopped Ahead, you are staying put')
            board.basepaths[2] = 0  # I don't want to deal with 2 runners at the same base
        else:
            throwDist = polarDistance(dist, 90, angle, math.pi/2)
            guessThrowTime = .75 + (throwDist / guessThrowSpeed)
            if board.B2.controlled:
                print('Input anything to run to third, just hit enter to stay.')
                print('Checkpoint Time', round(time, 2), 'Run Time', round(runTime, 2), 'Estimated Throw Time', round(guessThrowTime, 2))
                choice = input('Run?')
                if choice:
                    running.append(board.B2)
                else:
                    board.basepaths[2] = 0
            else:
                if runTime < guessThrowTime + time:
                    running.append(board.B2)
                else:
                    board.basepaths[2] = 0
    if board.B1:
        runTime = (90 - board.basepaths[1]) / (20 + .5 * board.B1.speed)
        if board.force:
            if board.B1.controlled:
                print('Force play, you are running to second')
            running.append(board.B1)
        elif board.B2 and board.B2 not in running:
            if board.B1.controlled:
                print('Runner Stopped Ahead, you are staying put')
            board.basepaths[1] = 0
        else:
            throwDist = polarDistance(dist, 90 * math.sqrt(2), angle, math.pi / 4)
            guessThrowTime = .75 + (throwDist / guessThrowSpeed)
            if board.B1.controlled:
                print('Input anything to run to second, just hit enter to stay.')
                print('Checkpoint Time', round(time, 2), 'Run Time', round(runTime, 2), 'Estimated Throw Time', round(guessThrowTime, 2))
                choice = input('Run?')
                if choice:
                    running.append(board.B1)
                else:
                    board.basepaths[1] = 0
            else:
                if runTime < guessThrowTime + time:
                    running.append(board.B1)
                else:
                    board.basepaths[1] = 0
    if board.hitter:  # hitters always have to run
        if board.hitter.controlled:
            print('You are running to first')
        running.append(board.hitter)
    if None in running:  # Does not mean no one is running, but that a NoneType object snuck into the list
        print('woah there cowboy')  # I was having some trouble with it before
    return running


def adjudication(fielder, dist, angle, runners, throw, board, timeSinceCheckpoint, defense):  # Runs, Safe/Out calls
    runsScored = 0
    throwSpeed = (75 + fielder.field) * mphTOfts
    throwTime = .75 + (dist / throwSpeed)
    if throw == 0:  # Throw goes home
        runTime = (90 - board.basepaths[3]) / (20 + .5 * board.B3.speed)
        if runTime < throwTime + timeSinceCheckpoint:  # Safe at home
            if board.scoring == 'triple':  # this guy is the orignal hitter who came all the way around to score
                board.scoring = 'IPHR'
            runsScored += 1
            board.B3.R += 1
            board.B3.chargedTo.ER += 1
            if board.p >= 3:
                print('safe at home')
                print('run scores')
        else:  # Out at home
            if board.force:
                board.scoring = 'FC'
            board.outs += 1
            board.pitcher.OR += 1
            defense[1].stamScore += 1
            if board.p >= 3:
                print('out at home')
            if board.outs >= 3:
                return [0, 0, defense[2], runsScored, 0]
        board.B3 = None
        board.basepaths[3] = 0
    elif board.B3 and board.B3 in runners:  # This means throw isn't home, uncontested.
        board.basepaths[3] += (timeSinceCheckpoint + throwTime) * (20 + .5 * board.B3.speed)
        if board.basepaths[3] >= 90:
            if board.scoring == 'triple':
                board.scoring = 'IPHR'
            runsScored += 1
            board.B3.R += 1
            board.B3.chargedTo.ER += 1
            if board.p >= 3:
                print('run scores')
            board.basepaths[3] = 0
            board.B3 = None
    if throw == 3:
        runTime = (90 - board.basepaths[2]) / (20 + .5 * board.B2.speed)
        if runTime < throwTime + timeSinceCheckpoint:  # Safe at third
            if board.p >= 3:
                print('safe at third base')
            if board.scoring == 'double':
                board.scoring = 'triple'
            if board.B3 is None:
                board.B3 = board.B2
                board.basepaths[3] = (20 + .5 * board.B2.speed)*(throwTime + timeSinceCheckpoint - runTime)  # for next CP
                board.B2 = None
                board.basepaths[2] = 0
            else:  # Have to be treated as 2nd base for a bit here, this gets solved in FF (the one aidan is proud of)
                board.basepaths[2] = 90 + (20 + .5 * board.B2.speed) * (throwTime + timeSinceCheckpoint - runTime)
        else:
            if board.force:
                board.scoring = 'FC'
            if board.p >= 3:
                print('out at third base')
            board.outs += 1
            board.pitcher.OR += 1
            defense[1].stamScore += 1
            board.B2 = None
            board.basepaths[2] = 0
            if board.outs >= 3:
                return [0, 0, defense[2], runsScored, 0]
    elif board.B2 and board.B2 in runners:
        board.basepaths[2] += (timeSinceCheckpoint+throwTime) * (20 + .5 * board.B2.speed)
        if board.basepaths[2] >= 90 and board.B3 is None:
            if board.scoring == 'double':
                board.scoring = 'triple'
            board.B3 = board.B2
            board.basepaths[3] = board.basepaths[2] - 90
            board.basepaths[2] = 0
            board.B2 = None
    if throw == 2:
        runTime = (90 - board.basepaths[1]) / (20 + .5 * board.B1.speed)
        if runTime < throwTime + timeSinceCheckpoint:  # Safe at 2nd
            if board.p >= 3:
                print('safe at second base')
            if board.scoring == 'single':
                board.scoring = 'double'
            if board.B2 is None:
                board.B2 = board.B1
                board.basepaths[2] = (20 + .5 * board.B1.speed)*(throwTime + timeSinceCheckpoint - runTime)
                board.B1 = None
                board.basepaths[1] = 0
            else:
                board.basepaths[1] = 90 + (20 + .5 * board.B1.speed) * (throwTime + timeSinceCheckpoint - runTime)
        else:
            if board.p >= 3:
                print('out at second')
            if board.force:
                board.scoring = 'FC'
            board.outs += 1
            board.pitcher.OR += 1
            defense[1].stamScore += 1
            board.B1 = None
            board.basepaths[1] = 0
            if board.outs >= 3:
                return [0, 0, defense[2], runsScored, 0]
    elif board.B1 and board.B1 in runners:
        board.basepaths[1] += (timeSinceCheckpoint+throwTime) * (20 + .5 * board.B1.speed)
        if board.basepaths[1] >= 90 and board.B2 is None:
            if board.scoring == 'single':
                board.scoring = 'double'
            board.B2 = board.B1
            board.basepaths[2] = board.basepaths[1] - 90
            board.basepaths[1] = 0
            board.B1 = None
    if throw == 1:
        runTime = (90 - board.basepaths[0]) / (16 + .5 * board.hitter.speed)
        if runTime < throwTime + timeSinceCheckpoint:  # Safe at 1st
            if board.p >= 3:
                print('safe at first')
            board.force = False
            if board.scoring == 'out':
                board.scoring = 'single'
            if board.B1 is None:
                board.B1 = board.hitter
                board.basepaths[1] = (20 + .5 * board.hitter.speed)*(throwTime + timeSinceCheckpoint - runTime)
                board.hitter = None
                board.basepaths[0] = 0
            else:
                board.basepaths[0] = 90 + (20 + .5 * board.hitter.speed) * (throwTime + timeSinceCheckpoint - runTime)
        else:
            if board.p >= 3:
                print('out at first')
            if board.scoring == 'FC':
                board.scoring = 'DP'
            board.outs += 1
            board.pitcher.OR += 1
            defense[1].stamScore += 1
            board.hitter = None
            board.basepaths[0] = 0
            if board.outs >= 3:
                return [0, 0, defense[2], 0, 0]
            board.force = False
    elif board.hitter and board.hitter in runners:
        board.basepaths[0] += (timeSinceCheckpoint+throwTime) * (20 + .5 * board.hitter.speed)
        if board.basepaths[0] >= 90 and board.B1 is None:
            if board.scoring == 'out':
                board.scoring = 'single'
            board.B1 = board.hitter
            board.basepaths[1] = board.basepaths[0] - 90
            board.basepaths[0] = 0
            board.hitter = None
            board.force = False  # They got to first base
    # This bit is all for who has the ball now where
    if throw == 0:
        newDist = 0
        newAngle = 0
        receiver = defense[2]
    elif throw == 1:
        newDist = 90
        newAngle = 0
        receiver = defense[3]
    elif throw == 2:
        newDist = 90 * math.sqrt(2)
        newAngle = math.pi/4
        if angle >= math.pi/4:
            receiver = defense[4]
        else:
            receiver = defense[6]
    elif throw == 3:
        newDist = 90
        newAngle = math.pi/2
        receiver = defense[5]
    elif throw == 4:
        newDist = 60.6
        newAngle = 0
        receiver = defense[1]
    elif throw == 5:
        newDist = 90 * math.sqrt(2)
        newAngle = math.pi / 4
        if angle >= math.pi / 4:
            receiver = defense[4]
        else:
            receiver = defense[6]
    else:
        newDist = dist
        newAngle = angle
        receiver = fielder
    [newTime, addRuns] = fastForward(board)
    return [newDist, newAngle, receiver, runsScored+addRuns, newTime]


def prePickupRunnin(board, ogCheckpoint):  # For long hits,
    # best decision-making is made when hitters are treated for mose recent base
    runs = 0
    if board.B3:
        runTime = (90 - board.basepaths[3]) / (20 + .5 * board.B3.speed)
        if runTime < ogCheckpoint + .75:  # +.75 includes ball in glove but before release
            if board.scoring == 'triple':
                board.scoring = 'IPHR'
            if board.p >= 3:
                print('run scores pre-throw')
            runs += 1
            board.B3.R += 1
            board.B3.chargedTo.ER += 1
            board.basepaths[3] = 0
            board.B3 = None
    if board.B2 and board.B3 is None:
        runTime = (90 - board.basepaths[2]) / (20 + .5 * board.B2.speed)
        if runTime < ogCheckpoint + .75:
            if board.scoring == 'double':
                board.scoring = 'triple'
            board.B3 = board.B2
            board.basepaths[3] = board.basepaths[2] - 90
            board.basepaths[2] = 0
            board.B2 = None
    if board.B1 and board.B2 is None:
        runTime = (90 - board.basepaths[1]) / (20 + .5 * board.B1.speed)
        if runTime < ogCheckpoint + .75:
            if board.scoring == 'single':
                board.scoring = 'double'
            board.B2 = board.B1
            board.basepaths[2] = board.basepaths[1] - 90
            board.basepaths[1] = 0
            board.B1 = None
    if board.hitter and board.B1 is None:
        runTime = (90 - board.basepaths[0]) / (20 + .5 * board.hitter.speed)
        if runTime < ogCheckpoint + .75:
            if board.scoring == 'out':
                board.scoring = 'single'
            board.B1 = board.hitter
            board.basepaths[1] = board.basepaths[0] - 90
            board.basepaths[0] = 0
            board.hitter = None
            board.force = False
    return runs


def fastForward(board):  # If you got a text from Aidan late one night saying
    # "Holy shit holy shit, I got it, negative checkpoint time!" It was about this
    # Why this works and the problem it solves:
    # 0 outs, 1st and 2nd (B1 and B2), ball gets lined to center for a single, but B1 is faster than B2
    # Let's say the CF picks up the ball after B1 gets to second but before B2 gets to third, who is B2?
    # Can say keep B2 as B1, but leads to imperfect decision-making.
    # Case 1: Throw is to third base. Either runner is out (B2 is now None) or Safe (B2 becomes B3)
    # Either way B2 is now None and can be reassigned without a problem (this happens within adjudication()).
    # Case 2: the throw is not to 3rd, there's no way you can throw out B2 at third if B1 is already at 2nd,
    # He's just too close already... so we just push him there, and take the time off the checkpoint on the backside.
    runsScored = 0
    checkpointTime = 0
    # Find who needs the most time to fix the problem
    if board.basepaths[0] > 90 and board.B1:
        checkpointTime = (90 - board.basepaths[1]) / (20 + .5 * board.B1.speed)
    if (board.basepaths[1] > 90 and board.B2) or (board.basepaths[0] > 90 and board.B1 and board.B2):
        timeToGo = (90 - board.basepaths[2]) / (20 + .5 * board.B2.speed)
        if timeToGo > checkpointTime:
            checkpointTime = timeToGo
    if (board.basepaths[2] > 90 and board.B3) or (board.basepaths[1] > 90 and board.B2 and board.B3) or \
            (board.basepaths[0] > 90 and board.B1 and board.B2 and board.B3):
        timeToGo = (90 - board.basepaths[3]) / (20 + .5 * board.B3.speed)
        if timeToGo > checkpointTime:
            checkpointTime = timeToGo
    # Now push everyone forward by that much time
    if board.B3:
        board.basepaths[3] += checkpointTime*(20 + .5 * board.B3.speed)
        if board.basepaths[3] >= 90:
            if board.scoring == 'triple':
                board.scoring = 'IPHR'
            runsScored += 1
            if board.p >= 3:
                print('run scores on FF')
            board.B3.R += 1
            board.B3.chargedTo.ER += 1
            board.basepaths[3] = 0
            board.B3 = None
    if board.B2:
        board.basepaths[2] += checkpointTime*(20 + .5 * board.B2.speed)
        if board.basepaths[2] >= 90:
            if board.scoring == 'double':
                board.scoring = 'triple'
            board.basepaths[3] = board.basepaths[2] - 90
            board.basepaths[2] = 0
            board.B3 = board.B2
            board.B2 = None
    if board.B1:
        board.basepaths[1] += checkpointTime * (20 + .5 * board.B1.speed)
        if board.basepaths[1] >= 90:
            if board.scoring == 'single':
                board.scoring = 'double'
            board.basepaths[2] = board.basepaths[1] - 90
            board.basepaths[1] = 0
            board.B2 = board.B1
            board.B1 = None
    if board.hitter:
        board.basepaths[0] += checkpointTime * (20 + .5 * board.hitter.speed)
        if board.basepaths[0] >= 90:
            if board.scoring == 'out':
                board.scoring = 'single'
            board.basepaths[1] = board.basepaths[0] - 90
            board.basepaths[0] = 0
            board.B1 = board.hitter
            board.hitter = None
    return [-checkpointTime, runsScored]


def changePitcher(lineup, board):  # Brings in a reliever
    try:  # Can only use Available pitchers, so there might not be enough and it'll throw an error
        if board.inning >= 9:  # Closer, bring in the best reliever available
            newPitcher = lineup.bullpen[lineup.bullpen['Available'] == True].iloc[0]['Name']
            newPitcher.available = False
        elif board.inning == 8:  # Setup man, 2nd best
            newPitcher = lineup.bullpen[lineup.bullpen['Available'] == True].iloc[1]['Name']
            newPitcher.available = False
        else:  # 3rd best for the rest
            hold = lineup.bullpen[lineup.bullpen['Available'] == True].iloc[2]
            if hold is not None:
                newPitcher = hold['Name']
            else:
                raise IndexError
            newPitcher.available = False
        newPitcher.stamScore = RPstam
        lineup.bullpen['Available'] = [i.available for i in list(lineup.bullpen['Name'])]
    except IndexError or TypeError:  # Brings in tomorrow's starter and pushes the rotation up a day.
        # print('Caught an error')
        # print(board.inning, lineup.bullpen)
        newPitcher = lineup.rotation.iloc[lineup.rotMarker]['Name']
        lineup.rotMarker = (lineup.rotMarker + 1) % 5
        newPitcher.stamScore = 100
    if board.p >= 2:
        print(newPitcher, 'is entering the game')
    lineup.dAlign[1] = newPitcher  # Actually puts them in the game
    lineup.relieversUsed.append(newPitcher)


def stealDec(board):  # Runners may steal second
    if not board.B1 or board.B2:
        return False
    if board.outs == 1:  # There's a thing about avoiding outs 1 and 3 at second (or out 3 at 3rd)
        return odds(.05 * .5 * board.B1.speed)
    elif board.outs == 0:
        return odds(.025 * .5 * board.B1.speed)
    else:
        return odds(.025 * .5 * board.B1.speed)


def stealAdj(board, catcher, spiked):  # Steal adjudication
    if board.outs >= 3:  # Doesn't matter
        return
    if odds(.25+(.05*catcher.field)) and not spiked:
        popTime = 2.2 - (.02 * catcher.field)
    elif not spiked:  # Throw is off-line
        popTime = 4
    else:  # Spiked
        popTime = 3.2 - (.02 * catcher.field)
    runTime = (90 - board.basepaths[1]) / (20 + .5 * board.B1.speed)
    if runTime < popTime:  # the running for pitch time has already been done
        board.B1.SB += 1
        if board.p >= 2:
            print('stolen base')
        board.B2 = board.B1
        board.basepaths[2] = 0
    else:
        board.B1.CS += 1
        if board.p >= 2:
            print('caught stealing')
        board.outs += 1
        board.pitcher.OR += 1
    board.B1 = None
    board.basepaths[1] = 0


def statsHelp(res, hitter, pitcher):  # For balls in play
    if res == 'single':
        hitter.H += 1
        hitter.TB += 1
        pitcher.H += 1
    elif res == 'double':
        hitter.H += 1
        hitter.TB += 2
        pitcher.H += 1
    elif res == 'triple':
        hitter.H += 1
        hitter.TB += 3
        pitcher.H += 1
    elif res == 'IPHR':
        hitter.H += 1
        hitter.TB += 4
        pitcher.H += 1
