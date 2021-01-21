class Score:
    def __init__(self, playerscore=0):
        self.playerscore = playerscore
        self.tempscore = 0

    def change(self, alter, temporary=True, reset=False):
        if reset:
            self.tempscore = 0
        else:
            if temporary:
                self.tempscore += alter
            else:
                self.playerscore += self.tempscore


# P1 = Score(0)
# P1.change(500)
# print(P1.tempscore)
# print(P1.playerscore)
# P1.change(1000)
# print(P1.tempscore)
# P1.change(None, False)
# print(P1.playerscore)
# P1.change(None, True, True)
# print(P1.tempscore)
# print(P1.playerscore)
# P1.change(100)
# P1.change(None, False)
# print(P1.playerscore)




# def bank(x, storage):
#     if x:
#         storage += 100
#     else:
#         storage += -300
#     return storage
#
#
# P1 = Score(0)
# P1.change(bank(False, 0))
#
# print(P1.playerscore)

# def bank(x, storage):
#     if x:
#         storage += 100
#     else:
#         storage += -300
#     return storage
#
#
# P1 = Score(0)
#
# # Upon running both of these print statements, I found that using the change method inside of a
# # print function still affects the value after and outside of the print. I am surprised,
# # though I really shouldn't be, because to get the value of the method, it still has to run it.
# # I will remember this when I make the view functions, remembering to undo any changes made
# # as a result of printing.
#
# print(P1.change(bank(False, 0)))
# print(P1.playerscore)
