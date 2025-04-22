from random import randint

def coinflip():
    flip = randint(1,2)
    if flip == 1:
        return "Heads"
    else:
        return "Tails"