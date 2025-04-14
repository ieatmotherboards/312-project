import request
from random import randint
outcomes = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,0.0]
red = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
black = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
'''
Rules
Single number bet pays 35 to 1. Also called “straight up.”
Double number bet pays 17 to 1. Also called a “split.” 
Three number bet pays 11 to 1. Also called a “street.”
Four number bet pays 8 to 1. Also called a “corner bet.”
Five number bet pays 6 to 1. Only one specific bet which includes the following numbers: 0-00-1-2-3. Ethan Dumbes this 5Number
Six number bets pays 5 to 1. Example: 7, 8, 9, 10, 11, 12. Also called a “line.”
Twelve numbers or dozens (first, second, third dozen) pays 2 to 1.
Column bet (12 numbers in a row) pays 2 to 1. 
18 numbers (1-18) pays even money. 
18 numbers (19-36) pays even money. 
Red or black pays even money. 
Odd or even bets pay even money.
'''
def spinWheel():
    spin=outcomes[randint(0,len(outcomes)-1)]
    return spin

def handlebets(betList): #{name:name,betType: type of bet (odd/even/red/black/num/etc ...), betAmmount: ammountOfBet,numbers: [allNumbers]}
    outcome=spinWheel()
    out={}
    out['House']=0
    winningBets=[]
    winningBets.append(outcome)
    if outcome in red:
        winningBets.append('Red')
    elif outcome in black:
        winningBets.append('Black')
    
    if outcome <= 12 and outcome >0:
        winningBets.append('First12')
    elif outcome > 12 and outcome<=24:
        winningBets.append('Second12')
    elif outcome >24 and outcome <= 36:
        winningBets.append("Third12")
    
    if outcome>0 and outcome <=18:
        winningBets.append('First18')
    elif outcome >18 and outcome <=36:
        winningBets.append('Second18')

    if outcome not in [0,0.0]:
        if outcome %2 ==0:
            winningBets.append('Even')
        else:
            winningBets.append('Odd')
    for bet in betList:
        Better=bet['name']
        BetType=bet['betType']
        Ammount=bet['betAmmount']

        if BetType == 'Straight up':
            if outcome == bet['numbers']:
                out['House']=(out['House']-(36*Ammount))
                out[Better]=36*Ammount
            else:
                out['House']=(out['House']+Ammount)
                out[Better]=(-1*Ammount)
        elif BetType == "Split":
            if outcome in bet['numbers']:
                out['House']=(out['House']-(18*Ammount))
                out[Better]=18*Ammount
            else:
                out['House']=(out['House']+Ammount)
                out[Better]=(-1*Ammount)
        elif BetType == 'Street':
            if outcome in bet['numbers']:
                out['House']=(out['House']-(12*Ammount))
                out[Better]=12*Ammount
            else:
                out['House']=(out['House']+Ammount)
                out[Better]=(-1*Ammount)
        elif BetType == 'Corner bet':
            if outcome in bet['numbers']:
                out['House']=(out['House']-(9*Ammount))
                out[Better]=9*Ammount
            else:
                out['House']=(out['House']+Ammount)
                out[Better]=(-1*Ammount)
        elif BetType == '5Number':
            if outcome in bet['numbers']:
                out['House']=(out['House']-(7*Ammount))
                out[Better]=7*Ammount
            else:
                out['House']=(out['House']+Ammount)
                out[Better]=(-1*Ammount)
        elif BetType == 'Line':
            if outcome in bet['numbers']:
                out['House']=(out['House']-(6*Ammount))
                out[Better]=6*Ammount
            else:
                out['House']=(out['House']+Ammount)
                out[Better]=(-1*Ammount)
        elif BetType == 'First12':
            if BetType in winningBets:
                out['House']=(out['House']-(3*Ammount))
                out[Better]=3*Ammount
            else:
                out['House']=(out['House']+Ammount)
                out[Better]=(-1*Ammount)
        elif BetType == 'Second12':
            if BetType in winningBets:
                out['House']=(out['House']-(3*Ammount))
                out[Better]=3*Ammount
            else:
                out['House']=(out['House']+Ammount)
                out[Better]=(-1*Ammount) 
        elif BetType == 'Third12':
            if BetType in winningBets:
                out['House']=(out['House']-(3*Ammount))
                out[Better]=3*Ammount
            else:
                out['House']=(out['House']+Ammount)
                out[Better]=(-1*Ammount)
        elif BetType == "First18":
            if BetType in winningBets:
                out['House']=(out['House']-(2*Ammount))
                out[Better]=2*Ammount
            else:
                out['House']=(out['House']+Ammount)
                out[Better]=(-1*Ammount)
        elif BetType == "Second18":
            if BetType in winningBets:
                out['House']=(out['House']-(2*Ammount))
                out[Better]=2*Ammount
            else:
                out['House']=(out['House']+Ammount)
                out[Better]=(-1*Ammount)
        elif BetType == "Black":
            if BetType in winningBets:
                out['House']=(out['House']-(2*Ammount))
                out[Better]=2*Ammount
            else:
                out['House']=(out['House']+Ammount)
                out[Better]=(-1*Ammount)
        elif BetType == "Red":
            if BetType in winningBets:
                out['House']=(out['House']-(2*Ammount))
                out[Better]=2*Ammount
            else:
                out['House']=(out['House']+Ammount)
                out[Better]=(-1*Ammount)
        elif BetType == 'Odd':
            if BetType in winningBets:
                out['House']=(out['House']-(2*Ammount))
                out[Better]=2*Ammount
            else:
                out['House']=(out['House']+Ammount)
                out[Better]=(-1*Ammount)
        elif BetType == 'Even':
            if BetType in winningBets:
                out['House']=(out['House']-(2*Ammount))
                out[Better]=2*Ammount
            else:
                out['House']=(out['House']+Ammount)
                out[Better]=(-1*Ammount)
    return out

