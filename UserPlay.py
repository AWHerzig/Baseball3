from Players import *
from League import *
from DirectoryWide import *


def userStartup():
    print('1 for Hitter, 2 for Pitcher, 3 for GM, 4 for CPU SIM')
    user1 = input('What is your choice?')
    if user1 == '1':
        player = buildAHitter()
    elif user1 == '2':
        print('Input anything to be a Starting Pitcher, just hit enter to be a Reliever')
        user2 = input('What is your choice?')
        if user2:
            player = buildAPitcher('SP')
        else:
            player = buildAPitcher('RP')
    elif user1 == '3':
        player = pickATeam()
        try:
            choiceB = int(input('0 for small budget (150), 1 for average (250), 2 for big budget (350), blank for given'))
            if choiceB > 2 or choiceB < 0:
                raise ValueError
            player.budget = 150 + (100 * choiceB)
        except ValueError:
            pass
    else:
        player = None
    return player


def userStartup2(player):
    if isinstance(player, Hitter):
        user3 = input('Input anything to be able to pick your team, just hit enter to be assigned team')
        if user3:
            team = pickATeam()
        else:
            team = random.choice(NLt+ALt)
        team.hitters.reset_index(drop=True, inplace=True)
        team.hitters.loc[12] = numpy.array([player, player.pos, player.secondary, player.overall, player.offense,
                                            player.available], dtype=object)
        team.hitters.sort_values(['Overall', 'Offense'], inplace=True, ascending=False)
        print(team)
        print(team.hitters)
        dud = input('Hit enter to advance')
    elif isinstance(player, Pitcher):
        user3 = input('Input anything to be able to pick your team, just hit enter to be assigned team')
        if user3:
            team = pickATeam()
        else:
            team = random.choice(NLt + ALt)
        if player.pos == 'SP':
            team.rotation.reset_index(drop=True, inplace=True)
            team.rotation.loc[4] = numpy.array([player, player.hand, player.arStr, player.overall,
                                                player.extension], dtype=object)
            team.rotation.sort_values(['Core', 'Extension'], inplace=True, ascending=False)
            print(team)
            print(team.rotation)
            dud = input('Hit enter to advance')
        else:
            team.bullpen.reset_index(drop=True, inplace=True)
            team.bullpen.loc[7] = numpy.array([player, player.hand, player.arStr, player.overall,
                                               player.extension, player.available], dtype=object)
            team.bullpen.sort_values(['Core', 'Extension'], inplace=True, ascending=False)
            print(team)
            print(team.bullpen)
            dud = input('Hit enter to advance')
    elif isinstance(player, Team):
        player.controlled = True
        if input('Input anything to set your own FA scouting evaluations, blank to use old front offices values.'):
            valStr = ['Contact', 'Power', 'Vision', 'Hitter Field/Speed', 'Control', 'Velocity', 'Movement', 'Pitcher Field/Speed', 'Prospect Boost']
            print('Standard is 1-3 for all of these, but tbh you can do anything you want, just a linear combination.')
            for i in range(9):
                try:
                    choice = int(input('How much will you value '+valStr[i]+'?'))
                except ValueError:
                    print('Bad input, set to 0')
                    choice = 0
                player.values[i] = choice
        dud = input('There is no prospect draft your first year bc nobody has wins from last year.')


def buildAHitter():
    name = input('What is your player\'s name? (Max 15 characters)')
    pos1 = None
    pos2 = None
    while pos1 is None and pos2 is None:
        try:
            pos1 = input('What is your primary position? (C, 1B, 2B, 3B, SS, LF, CF, RF)')
            if pos1 == 'C':
                pos1 = 'C '
            pos2 = input('What is your secondary position? (C, 1B, 2B, 3B, SS, LF, CF, RF)')
            if pos2 == 'C':
                pos2 = 'C '
            if pos1 not in posNotation and pos2 not in posNotation:
                raise ValueError
        except ValueError:
            print('Faulty input... somewhere don\'t ask me')
            pos1 = None
            pos2 = None
            continue
    handPick = input('Input anything for Left Handed, just hit enter for Right Handed')
    hand = 1 if handPick else -1
    player = Hitter(name, pos1, hand=hand, controlled=True)
    (player.con, player.pow, player.vis, player.field, player.speed) = (4, 4, 4, 4, 4)
    (player.secondary, player.age, player.contract) = (pos2, 1, [3, 2])
    player.offense = player.con + player.pow + player.vis
    player.overall = player.offense + player.field + player.speed
    return player


def buildAPitcher(pos):
    name = input('What is your player\'s name? (Max 15 characters)')
    handPick = input('Input anything for Left Handed, just hit enter for Right Handed')
    hand = 1 if handPick else -1
    arsenal = []
    print('You will get 2 Pitches')
    for i in range(len(list(pitches.keys()))):
        if list(pitches.keys())[i] not in arsenal:
            print(i, list(pitches.keys())[i])
    for i in range(2):
        pick = int(input('Input the number corresponding to the pitch you want'))
        arsenal.append(list(pitches.keys())[pick])
    print(arsenal)
    player = Pitcher(name, pos, hand=hand, controlled=True)
    (player.cont, player.velo, player.move, player.field, player.speed) = (4, 4, 4, 4, 4)
    (player.age, player.contract, player.arsenal) = (1, [3, 2], arsenal)
    player.arStr = ''
    for i in player.arsenal:
        player.arStr = player.arStr + i[0:2]
    player.overall = player.cont + player.velo + player.move
    player.total = player.overall + player.field + player.speed
    pre = True
    print('Presets (pitch type and location aim) for pitching will make this way more enjoyable, I recommend using '
          'them. As many as u want but Id say no more than 5 for space')
    while pre:
        pre = input('Input anything to add a preset, nothing to skip')
        if not pre:
            break
        print(player.arsenal)
        try:
            choice = int(input('Which pitch do you want to use, first is 0, second is 1, etc.'))
            pType = player.arsenal[choice]
        except IndexError:  # If user messes up, so the entire thing doesnt come crashing down
            print('bad input')
            continue
        try:
            xPick = float(input('X-coordinate aim?'))
            yPick = float(input('Y-coordinate aim?'))
        except ValueError:
            print('bad input')
            continue
        player.presets.append([pType, xPick, yPick])
    return player


def pickATeam():
    allTeams = NLt+ALt
    for i in range(30):
        print(i, allTeams[i])
    pick = int(input('Input the number corresponding to the team you want'))
    team = allTeams[pick]
    return team



