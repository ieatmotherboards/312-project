from random import randint


def createDeck():
    #Creates Deck for blackJack game
    Suits=['Hearts','Diamonds','Clubs','Spades']
    Cards=['2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace']
    deck=[]
    for suit in Suits:
        for card in Cards:
            deck.append((suit,card))
    return deck

def dealCard(deck):
    #In deck created
    #Out card that is "drawn"
    out=deck.pop(randint(0,len(deck)-1))
    return(out)

def calcScore(hand):
    #In hand
    #Out current Score
    score=0
    aceHold=[]
    for suit, card in hand:
        if card == 'Ace':
            aceHold.append((suit,card))
        else:
            if card in ['Jack','Queen','King']:
                score+=10
            else:
                score+=(int(card))
    aces=len(aceHold)
    for ace in aceHold:
        if aces * 11 + score <= 21:
            score+=(aces*11)
            break
        else:
            aces=aces-1
            score+=1
    return score

def handleDealer(dealerHand,deck):
    #In dealers starting hand and deck
    #out dealers ending hand
    while calcScore(dealerHand) <=16:
        dealerHand.append(dealCard(deck))
        print(calcScore(dealerHand))
    return dealerHand

def calcWinnder(dealerHand,playerHand):
    #In DealersHand and PlayersHand
    #Out all related ot player the strings Push, Black Jack, Win, or Lose
    '''
    Push = draw (money back)
    Blak Jack = player black jack 1.5x bet 
    Win = player win 
    Lose = player Lose
    '''

    playerScore=calcScore(playerHand)
    dealerScore=calcScore(dealerHand)
    if playerScore ==21 and len(playerHand)==2:
        if dealerScore == 21 and len(dealerHand)==2:
            return "Push"
        else:
            return "Black Jack"
    elif playerScore > 21:
        return "Lose"
    elif dealerScore >21:
        return "Win"
    else:
        if playerScore > dealerScore:
            return "Win"
        elif playerScore < dealerScore:
            return "Lose"
        else:
            return "Push"



