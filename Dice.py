import random
random.seed(a=None, version=2)

class Dice:
    # I think I will be getting rid of the __init__ because I don't want this to be a class that you call. Throughout
    # the course of the game, you will only be changing the roll_storage and having two different instances of this
    # class might interfere with the values in the dictionary, if not at the very least be inconvenient to call a
    # new instance of the class each time the dice limit is updated.

    # def __init__(self, dice_limit, dice_type=range(1, 7)):
    #     self.dice_limit = dice_limit
    #     self.dicetype = dice_type

    roll_storage = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0
    }

    # This one is static because it does not directly change anything in the class, just provides a value.
    @staticmethod
    def diceroll(dice_type=range(1, 7)):
        return random.choice(dice_type)

    @classmethod
    def rollcup(cls, dice_limit):
        for x in Dice.roll_storage:
            Dice.roll_storage[x] = 0
        for x in range(1, dice_limit+1):
            Dice.roll_storage[Dice.diceroll()] += 1

    @classmethod
    def change(cls, dice_to_change, alt):
        Dice.roll_storage[dice_to_change] += alt
