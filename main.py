from Score import Score
from Dice import Dice
from os import system
import time

import random

random.seed(a=None, version=2)


class Storage: # what the fuck was i thinking
    kept_storage = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0
    }

    acc_rolled = []
    acc_kept = []

    selectable = {
        1: False,
        2: False,
        3: False,
        4: False,
        5: False,
        6: False
    }

    winmap = {}

    @classmethod
    def change(cls, dice_to_change, alt):
        Storage.kept_storage[dice_to_change] += alt

    @classmethod
    def approve(cls, dice_to_change, binary, reset=False):
        if reset:
            for x in Storage.selectable:
                Storage.selectable[x] = False
        else:
            Storage.selectable[dice_to_change] = binary

    @staticmethod
    # Because this is a static method, I assume this means that acc_rolled is not actually being changed. It only has
    # a different value inside of this method that is displayed because of the return statement.
    def accessible(viewing_rolled):
        Storage.acc_rolled.clear()
        Storage.acc_kept.clear()
        if viewing_rolled:
            for x in Dice.roll_storage:
                for xa in range(1, Dice.roll_storage[x] + 1):
                    Storage.acc_rolled.append(x)
            return Storage.acc_rolled
        else:
            for x in Storage.kept_storage:
                for xa in range(1, Storage.kept_storage[x] + 1):
                    Storage.acc_kept.append(x)
            return Storage.acc_kept

    @classmethod
    def farkle(cls):
        bust = 0
        determine(True, None)
        if not Storage.accessible(True):
            return False
        for f in Dice.roll_storage:
            if Dice.roll_storage[f] > 0:
                if not Storage.selectable[f]:
                    bust += Dice.roll_storage[f]
        if bust == len(Storage.accessible(True)):
            return True

    @classmethod
    def instant_w(cls, scoremap, player):
        Storage.winmap = dict(scoremap).copy()
        for cw in Storage.winmap:
            Storage.winmap[cw] = False
            if cw == player:
                Storage.winmap[cw] = True


def determine(evaluating, player_up):
    # This is a really cool built-in function I found called isinstance. It returns a True or False value
    # depending on if a value is an instance of a class. It feels a bit cheaty using something so OP,
    # so I wanted to make a module of the same functionality by myself. I am thinking this has something
    # to do with the jumbled mess that includes 'main' printed when you type print(Class). For now, as
    # much as I hate using shortcuts, I won't let this stall me.

    # Actually, it seems like it's not really necessary.

    # if not isinstance(player_up, Score):
    #     raise ValueError

    # 2 pairs of 3
    on3 = 0
    if not evaluating:
        for x in Storage.kept_storage:
            if Storage.kept_storage[x] == 3:
                on3 += 1
        if on3 == 2:
            player_up.change(2500)
            for x in Storage.kept_storage:
                if Storage.kept_storage[x] == 3:
                    Storage.change(x, -(Storage.kept_storage[x]))

    # 3 pairs of 2
    on2 = 0
    if evaluating:
        for x in Dice.roll_storage:
            if Dice.roll_storage[x] == 2:
                on2 += 1
        if on2 == 3:
            for s in Dice.roll_storage:
                if Dice.roll_storage[s] == 2:
                    Storage.approve(s, True)
    else:
        for x in Storage.kept_storage:
            if Storage.kept_storage[x] == 2:
                on2 += 1
        if on2 == 3:
            player_up.change(1500)
            for x in Storage.kept_storage:
                if Storage.kept_storage[x] == 2:
                    Storage.change(x, -(Storage.kept_storage[x]))

    onstraight = 0
    if evaluating:
        for x in Dice.roll_storage:
            if Dice.roll_storage[x] == 1:
                onstraight += 1
        if onstraight == 6:
            for x in Dice.roll_storage:
                if Dice.roll_storage[x] == 1:
                    Storage.approve(x, True)
    else:
        for x in Storage.kept_storage:
            if Storage.kept_storage[x] == 1:
                onstraight += 1
        if onstraight == 6:
            for x in Storage.kept_storage:
                if Storage.kept_storage[x] == 1:
                    player_up.change(3000)
                    Storage.change(x, - (Storage.kept_storage[x]))

    if evaluating:
        for x in Dice.roll_storage:
            if Dice.roll_storage[x] >= 3:
                if x == 1 and Dice.roll_storage[x] == 6:
                    break
                else:
                    Storage.approve(x, True)
            else:
                # Before, every value passed this check. I realized this is because I wrote x == 1 or 5. While this
                # would intuitively seem correct, what that actually means is if x is equal to 1 OR if 5... is 5?
                # The 5 is 5 thing is also like saying while True, it's just a True filler value almost. Instead,
                # we be more specific by making sure both requirements are boolean checks.
                if x == 1 or x == 5:
                    if Dice.roll_storage[x] > 0:
                        Storage.approve(x, True)

    else:
        # Okay, so I just realized the reason this series of if statements doesn't work past 3 is because if I get
        # 4 3's, let's say, the if statement says, 'okay, there's not exactly 3, so he doesn't pass this check.' To
        # fix this, all I have to do is make them greater than or equal to, like I intended the program to do in the
        # first place. Stupid mistake.
        for x in Storage.kept_storage:
            if Storage.kept_storage[x] >= 3:
                if Storage.kept_storage[x] >= 4:
                    if Storage.kept_storage[x] >= 5:
                        if Storage.kept_storage[x] == 6:
                            player_up.change(4 * (x * 100))
                            Storage.change(x, -(Storage.kept_storage[x]))
                        else:
                            player_up.change(3 * (x * 100))
                            Storage.change(x, -(Storage.kept_storage[x]))
                    else:
                        player_up.change(2 * (x * 100))
                        Storage.change(x, -(Storage.kept_storage[x]))
                else:
                    if x == 1:
                        player_up.change(1000)
                        Storage.change(x, -(Storage.kept_storage[x]))
                    else:
                        player_up.change(x * 100)
                        Storage.change(x, -(Storage.kept_storage[x]))
            else:
                if x == 1 or x == 5:
                    if Storage.kept_storage[x] > 0:
                        if x == 1:
                            player_up.change(100 * Storage.kept_storage[x])
                            Storage.change(x, -(Storage.kept_storage[x]))
                        if x == 5:
                            player_up.change(50 * Storage.kept_storage[x])
                            Storage.change(x, -(Storage.kept_storage[x]))


def select():
    brk = False
    while True:
        try:
            if brk:
                break
            Storage.approve(None, False, True)
            while True:
                clear()
                print('On the table are: ', Storage.accessible(True))
                print('You are choosing to score with: ', Storage.accessible(False))
                # Before, I was getting an output from the following print statements that said

                # [ ((whatever dice I rolled)) ]
                # On the table are: None
                # []
                # You are choosing to score with: None

                # I think this is because the value being returned from accessible was a print() statement, meaning it
                # would print, print(return). Printing a print statement returns None, which is why there are 'None'
                # 'on the table'. The reason why the list comes before the text, though, is because Python works just
                # like a math problem. It simplifies whatever is the most embedded inside parentheses first, so we have
                # "first, the function wants me to print my list, then print our text and the returned value from that
                # function." Here is an example I made:

                # def test(list):
                #     return print(list)
                # print(print(test([3])))
                # >>> [3]
                # >>> None
                # >>> None
                determine(True, None)

                if Dice.roll_storage[1] == 6:
                    brk = True
                    break

                request = int(input('Choose the dice you wish to score with, or 0 to confirm selection: '))
                if request > 0:
                    if request > 6 or request == 0:
                        print("We don't use that dice here, moron.")
                        time.sleep(1)
                        continue
                    elif Dice.roll_storage[request] == 0:
                        print('That dice is not available.')
                        time.sleep(1)
                        continue
                    if Storage.selectable[request]:
                        Dice.change(request, -1)
                        Storage.change(request, 1)
                        continue
                    else:
                        print('The dice you chose has no possible scoring combinations.')
                        time.sleep(1)
                        continue
                else:
                    if request < -6:
                        print("You can't remove a dice that doesn't exist.")
                        time.sleep(1)
                        continue
                    elif request == 0:
                        if Storage.acc_kept:
                            brk = True
                            break
                        else:
                            print("You must select a dice.")
                            continue
                    elif Storage.kept_storage[request - (request * 2)] == 0:
                        print('That dice is not in your scoring selection.')
                        time.sleep(1)
                        continue
                    else:
                        Dice.change(request - (request * 2), 1)
                        Storage.change(request - (request * 2), -1)
                        continue
        except ValueError:
            print("That's not how ya' do that.")
            time.sleep(1)
            continue


def clear():
    _ = system('cls')


# GAME START ###########################################################################################################
system('color 02')
clear()

print("Welcome to Farkle! I'm surprised I haven't given up on this game yet!")
time.sleep(2)


# ADD EASTER EGG CODE HERE
players = 0
easteregg = False

while True:
    clear()
    try:
        players = input("Select 2 to 6 players to begin: ")
        if players == '09232020' or players == '9232020' or players == '092320' or players == '92320':
            easteregg = True
            print('... Strange.')
            time.sleep(2)
            continue
        else:
            players = int(players)
        if players < 2:
            print("At least 2 players are needed to start.")
            time.sleep(.4)
            continue
        if players > 6:
            print("The player limit is 6.")
            time.sleep(.4)
            continue
        else:
            time.sleep(.4)
            break
    except ValueError:
        print("Please enter an integer.")
        time.sleep(.4)
        continue

goal = 10000
while True:
    clear()
    try:
        goal = input("Select the score you would like to play to, or leave blank for 10000: ")
        if not goal:
            goal = 10000
            time.sleep(.4)
            print("Game starting... ")
            time.sleep(1.5)
            break
        else:
            goal = int(goal)
            if goal > 50000 or goal < 1000:
                print("Well... have fun?")
                print("Game starting... ")
                time.sleep(1.5)
            break
    except ValueError:
        print("Please enter an integer.")
        time.sleep(.4)
        continue

# Naming these variables and assigning them set in stone is not the most efficient choice. Looking at it, I realize that
# I could NOT name these manually and instead use a for statement that assigns x in range (1, players+1) to Score(0).
# At the very start of this game as mentioned in Blackjack, I used to try using dicecount1 to represent the number of
# '1' dice. Relying on the name of the variable to create a relation between data is completely ineffective. The same idea
# kind of applies here. The more I think about this though I'm sure I could refine my explanation. Okay, so the name P1
# and P2 and so on does not mean anything, it just acts as a way to access a certain instance of Score. Assigning it a
# variable is not necessary as long as we have some way to access the instance, like through indexing a list or
# dictionary. The actual relationship we wanted to achieve here is have each instance correspond to a player. We want
# each instance to instead directly relate to the player it represents, so when we see that an instance has the highest
# score, we can print the key that accesses that instance (the player number).
P1 = Score(0)  # This also makes me want to die, I could've just made rotationbasis [Score(0), Score(0)] and so on
P2 = Score(0)
P3 = Score(0)
P4 = Score(0)
P5 = Score(0)
P6 = Score(0)

# Using a for statement to assign the values to Score(0), I could get rid of these and actually, use only the data for
# the players that I need, meaning I could add as many players as the user wanted.
rotationbasis = (P1, P2, P3, P4, P5, P6)
scoreinstances = {
}
# This is actually pretty similar looking to what I proposed replacing. But instead of the redundant rotationbasis,
# we just directly assign the value to Score(0). I thought that the instance of a class could only exist if assigned a
# name, but really, that is stupid because CALLING Score(0) is what makes that instance 'exist', as long as it is ever
# accessible again (like by assigning it as the value to a key (int) in a dictionary).
for s in range(1, players+1):
    scoreinstances[s] = rotationbasis[s - 1]

# I could make the function play(players) where players would be defined in a main function outside of the play call.
# I look at it like, the entirety of this program should be a shell that changes what it does based on outside filling.
# What I mean by this is all this program really does is keep score and determine who has won. 'Who' in that sentence
# is important because that is the filling, the players is variable, (along with the score goal and the dice sides).
havetied = False
instantwin = False

# The while True is here so the program repeats the for statement once it is player one's turn again.
while True:
    clear()

    if instantwin:
        # I think I see another problem here involving data to variable relation. I suspect this because we would want
        # to add a variable to Score here that tells if instant win is true, but there's no way for us to check that
        # relation when we are not currently iterating that instance. What we could do, though, is after the dice are
        # rolled use a for loop to check each instance of Score to see if Score.instantwin is true. Once it find something
        # and breaks the current playing loop, we would simply do the same check in place of if instantwin and run the
        # then block with respect to x. This would save us from having to assign a value to the player with the win
        # (in winmap) and we could get rid of the instantwin variable above.
        # READ: I need to add that making a dictionary storing if the player won is not necessary. Not only would this
        # limit us to 6 players, but we can just add another piece of information to the Score instance. I didn't do this
        # in the first place because I thought we would have to have scoreinstance[1] for example, relate to both Score(0)
        # AND True or False. I realize now that Score(0) is like a big container for variables anyway, hence why we can
        # access tempscore and playerscore.
        castimir = []
        for iw in Storage.winmap:
            if Storage.winmap[iw]:
                castimir.append(iw)
        print("Fear player {}, for they have just gotten...".format(castimir))
        time.sleep(2)
        system('color 4')
        print("Ultra Snake Eyes.")
        time.sleep(6)
        raise ZeroDivisionError
    else:
        proceed = False

        # Again, here, we don't need another dictionary here to store which players have over 10,000 points. Actually,
        # we don't even need to keep track of which players have over 10000 points, just if any do so we can execute
        # the next chunk of code. Making a list of just people who have 10000 points but not who has the highest score
        # is redundant.
        winners = {}
        for w in scoreinstances:
            if scoreinstances[w].playerscore >= goal:
                proceed = True
                winners[w] = scoreinstances[w]

        # I am doing this as good practice to reduce the amount of code that needs to be run per loop. All the stuff
        # below does not apply if nobody has reached 10000 points.
        if proceed:
            scoreinstances.clear()

            # I am going to see if I can make my own max function that works when classes are the values, but you want
            # an integer inside the class
            judge = {}
            for p in winners:
                judge[p] = winners[p].playerscore

            for r in winners:
                if winners[r].playerscore == max(judge.values()):
                    scoreinstances[r] = rotationbasis[r - 1]

            if len(scoreinstances) == 1:
                for how in scoreinstances:
                    print('Player {} reached {} points! Congratulations!'.format(how, scoreinstances[how].playerscore))
                time.sleep(3)
                if easteregg:
                    # EASTER EGG WILL ACTIVATE HERE <---
                    system('color D')
                    print('\n')
                    print("Happy Birthday, Congratulations")
                    time.sleep(2)
                    system('color 6')
                    print("Happy Birthday, With Salutations")
                    time.sleep(2)
                    system('color 1')
                    print("Happy Birthday, May Your Sky Stay Blue,")
                    time.sleep(2)
                    system('color 4')
                    print("Happy Birthday to You")
                    time.sleep(6)
                raise ZeroDivisionError
            if len(scoreinstances) > 1:
                if havetied:
                    print("Christ, again?! Alright, next round.")
                    time.sleep(1.5)
                else:
                    times = 0
                    print("Players", end=' ')
                    if len(scoreinstances) > 2:
                        for p in scoreinstances:
                            times += 1
                            if times == len(scoreinstances):
                                print("and {} are tied with {} points.".format(p, scoreinstances[p].playerscore))
                                break
                            else:
                                print("{}, ".format(p), end='')
                    if len(scoreinstances) == 2:
                        for p in scoreinstances:
                            times += 1
                            if times == len(scoreinstances):
                                print("and {} are tied with {} points".format(p, scoreinstances[p].playerscore))
                                break
                            else:
                                print("{} ".format(p), end='')

                    print("Well, I guess you guys are special. A tiebreaker round will be played between the {} of you. "
                          "The person with the highest score afterwards will win, if you don't tie again, for God's sake."
                          .format(len(scoreinstances)))
                    time.sleep(3)

                    havetied = True
                    draw = True

    for x in scoreinstances:
        if instantwin:
            break

        clear()

        print("Player {}'s turn.".format(x))
        print("Current score: {}".format(scoreinstances[x].playerscore))
        time.sleep(2)

        Dice.rollcup(6)
        if Storage.farkle():
            print('On the table are {}'.format(Storage.accessible(True)))
            print('Damn, you threw the gun before you even shot him.')
            scoreinstances[x].change(None, None, True)
            continue

        while True:

            select()

            if Dice.roll_storage[1] == 6:
                instantwin = True
                Storage.instant_w(scoreinstances, x)
                break

            determine(False, scoreinstances[x])
            print('You will earn {} points and bring your score to {}.'
                  .format(scoreinstances[x].tempscore, (scoreinstances[x].tempscore + scoreinstances[x].playerscore)))

            tact = input("Type 'roll' to re-roll your leftover dice, or 'end' to end your turn: ")
            if tact == 'roll':
                # I used the length of accessible and not acc_rolled because accessible is a static method and does not
                # actually change acc_rolled, only class and self methods do that. The list we want is returned by this
                # method, so I look at the length of that.
                if len(Storage.accessible(True)) == 0:
                    Dice.rollcup(6)

                    determine(True, None)
                    if Storage.farkle():
                        clear()
                        print('On the table are {}'.format(Storage.accessible(True)))
                        time.sleep(1)
                        print('Farkle!')
                        time.sleep(2)

                        print("Current score: {}".format(scoreinstances[x].playerscore))
                        time.sleep(1)
                        scoreinstances[x].change(None, None, True)
                        break

                    continue

                else:
                    Dice.rollcup(len(Storage.accessible(True)))

                    determine(True, None)
                    if Storage.farkle():
                        clear()
                        print('On the table are {}'.format(Storage.accessible(True)))
                        time.sleep(1)
                        print('Farkle!')

                        time.sleep(2)
                        scoreinstances[x].change(None, None, True)
                        print("Current score: {}".format(scoreinstances[x].playerscore))
                        time.sleep(1)
                        break
                    continue

            if tact == 'end':
                scoreinstances[x].change(None, False)
                scoreinstances[x].change(None, None, True)
                print("Player {}'s score: {}".format(x, scoreinstances[x].playerscore))
                if scoreinstances[x].playerscore > goal:
                    time.sleep(1)
                    print("Player {} reached the {} point goal. All players with a remaining turn must exceed that score"
                          "to win or stay in the game!".format(x, goal))
                    time.sleep(2)
                else:
                    time.sleep(3)
                break
            else:
                print('Gosh, all you do is mess stuff up.')
                time.sleep(1)
                continue


# While I thought I was on the home stretch, it seems I am really not. My brain is a little fried, but I think it's best
# that I try to synthesize what's going wrong.

# 1. The tempscore is not being added to the player's total score (playerscore) correctly. Instead, tempscore overrides
# playerscore. Everything works as expected though in a test I have done inside of the Score module.
# 2. I need to ensure that the win is only counted after the end of each turn. This should not be too hard, though,
# because I have a while True loop already outside of my main for loop, used for returning to player one's turn.
# 3. The last thing I remember is that according to some websites, a farkle lets you keep doing your turn but forfeits
# any points you had previously earned(?). Even if this is the case, this isn't how I remember playing it in KCD, so
# I don't know if I really want to bother changing everything for this. Even if it will feel incomplete, this game
# should be a recreation of the way I know how to play it.
# 4. -FIXED- I remembered the fatal flaw I was having. If you get a roll you don't like, you can just type '0' and get a new
# roll. I think I can fix this by adding a check to see if the length of selected is greater than 0 before allowing a
# re roll.
# 5. Occasionally, you won't get a farkle when you're supposed to. I've seen this happen with the combination of three
# dice, 2, 4, and 6. I don't know if the numbers and the farkle not triggering have any kind of correlation, but I'll
# keep observing through the many test I know I will have to do throughout finishing this game.

# python C:\Users\volki\PycharmProjects\laboratory\DasFinalFarkle.py
