from Players import *
from League import *
from DirectoryWide import *


def userStartup():
    print('1 for Hitter, 2 for Pitcher, 3 for GM (SOON), 4 for CPU SIM')
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
        player.controlled = True
    else:
        player = None
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
        else:
            team.bullpen.reset_index(drop=True, inplace=True)
            team.bullpen.loc[7] = numpy.array([player, player.hand, player.arStr, player.overall,
                                               player.extension, player.available], dtype=object)
            team.bullpen.sort_values(['Core', 'Extension'], inplace=True, ascending=False)
            print(team)
            print(team.bullpen)


def buildAHitter():
    name = input('What is your player\'s name? (Max 15 characters)')
    pos1 = input('What is your primary position? (C, 1B, 2B, 3B, SS, LF, CF, RF)')
    if pos1 == 'C':
        pos1 = 'C '
    pos2 = input('What is your secondary position? (C, 1B, 2B, 3B, SS, LF, CF, RF)')
    if pos2 == 'C':
        pos2 = 'C '
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
    player.overall = player.cont + player.velo + player.move
    player.total = player.overall + player.field + player.speed
    return player


def pickATeam():
    allTeams = NLt+ALt
    for i in range(30):
        print(i, allTeams[i])
    pick = int(input('Input the number corresponding to the team you want'))
    team = allTeams[pick]
    return team



