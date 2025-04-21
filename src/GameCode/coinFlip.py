from random import randint

def Coinflip():
    flip=randint(1,2)
    if flip == 1:
        return "Heads"
    else:
        return "Tails"