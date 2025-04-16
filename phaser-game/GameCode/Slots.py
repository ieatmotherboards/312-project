import numpy as np
from random import randint
'''
Symbol Ideas For buying new symbols
Common Symbols:
Jesse
Stack Over Flow
Paul
Windows
Linux
Rare Symbols:
chatGpt (Ai violation)
Kris Schindler
Alan Hunt Drop Tables

Normal Slots symbols

Common Symbols:
Cherries
Lemon
Watermelon
Plum
Star
Rare Symbol:
Bar
Bell
Seven (7)
'''

normalSymbols=['Cherries','Lemon','Watermelon','Plum','Star','Bar','Seven','Bell']
cseSymbols=['Jesse','Stack over flow','Paul','Windows','Linux','chatGPT','Kris Schindler','Alan Hunt Drop Tables']

payouts={
    0:3,
    1:4,
    2:6,
    3:7,
    4:10,
    5:15,
    6:23,
    7:20
    }



def Slotmactine(playerDict):
    #In playerDIct = {'name':username, 'symbols':symbolName, 'bet':betAmount}
    #Out {'house':menyHosue made/lost, 'player': money username maade/lost, 'board':Output of array board for visuals}
    payout=0
    bet=playerDict['bet']
    slots=np.zeros((3,3))
    outMatrix = np.empty((3, 3), dtype=object)
    symbolList=playerDict['symbols']
    if symbolList == 'normal':
        symbols=normalSymbols
    elif symbolList == 'cse':
        symbols=cseSymbols
    for x in range(3):
        for y in range(3):
            #fills matrix with numbers to check for wins and later relate those numers to symbols
            num=randint(0,7)
            slots[x][y]=num
            outMatrix[x][y]=symbols[num]
    leftDiag=[slots[0][0],slots[1][1],slots[2][2]]
    rightDiag=[slots[2][0],slots[1][1],slots[0][2]]
    topRow=[slots[0][0],slots[1][0],slots[2][0]]
    midRow=[slots[0][1],slots[1][1],slots[2][1]]
    botRow=[slots[0][2],slots[1][2],slots[2][2]]
    moneyLines = [leftDiag,rightDiag,topRow,midRow,botRow]
    for row in moneyLines:
        if len(set(row))==1:
            symbol = row[0]
            multiplier=payouts[symbol]
            payout+=multiplier*bet

    out={}
    out['board']=outMatrix
    if payout==0:
        out['house']=bet
        out['player']=-1*bet
    else:
        out['house']=-1*payout
        out['player']=payout
    return out
    
    
if __name__ == '__main__':
    HouseProfit=0
    PlayerProfit=0
    houseWins=0
    bet=50
    input={'name':'Superice', 'symbols':'cse', 'bet':bet}
    simsToRun=1000000
    for x in range(simsToRun):
        temp=Slotmactine(input)
        #print(temp['board'])
        #print('----------------')
        if temp['house']>0:
            houseWins+=1
        #print(houseWins)
        
        HouseProfit+=temp['house']
        PlayerProfit+=temp['player']
        #print(HouseProfit)
        #print(PlayerProfit)
    print("Sims ran: "+ str(simsToRun))
    print("Bet Per Sim: "+str(bet))
    print('HouseProfit: '+str(HouseProfit))
    print('PlayerProfit: '+str(PlayerProfit))
    print("House Win Rate: "+ str(houseWins/simsToRun))

        

