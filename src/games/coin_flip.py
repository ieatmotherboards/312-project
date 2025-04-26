from random import randint

def coinflip():
    # returns: True if heads, False if tails
    flip = randint(0, 1)
    if flip == 1:
        return True # Heads
    else:
        return False # Tails