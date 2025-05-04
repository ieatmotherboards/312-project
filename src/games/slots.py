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
symbol_map = {
    "basic": ['Cherries', 'Lemon', 'Watermelon', 'Plum', 'Star', 'Bar', 'Bell', 'Seven'],
    "cse": ['Jesse', 'Stack over flow', 'Paul', 'Windows', 'Linux', 'chatGPT', 'Alan Hunt Drop Tables', 'Kris Schindler'],
    "emoji": ['🍒', '🍋', '🍉', '🍆', '⭐', '💰', '🔔', '7️'],
    "mines": ['Coal', 'Stone', 'Coin', 'Pickaxe', 'Crystal', 'Gold', 'Obsidian', 'Diamond']
}
# about 5% player edge
payouts = [3, 5, 8, 10, 15, 18, 22, 27]

def play_slots(bet : int):
    # In: player's bet
    # Out: {'board': numpy matrix of ints representing symbols, 'payout': player's payout (0 means lost bet)}
    payout = 0
    # 3x3 matrix for our slots. use like this: slot[y][x]
    slots = np.empty((3, 3), dtype=np.int64)
    # fills 3x3 matrix with random numbers between 0-7
    for y in range(3):
        for x in range(3):
            num = randint(0,7)
            slots[y][x] = num
    # lists with possible scoring patterns
    top_left_diagonal = [slots[0][0], slots[1][1], slots[2][2]]
    bot_left_diagonal = [slots[2][0], slots[1][1], slots[0][2]]
    top_row = [slots[0][0], slots[0][1], slots[0][2]]
    mid_row = [slots[1][0], slots[1][1], slots[1][2]]
    bot_row = [slots[2][0], slots[2][1], slots[2][2]]
    money_lines = {"top left": top_left_diagonal, "bot left": bot_left_diagonal, "top": top_row, "mid": mid_row, "bot": bot_row}
    winning_lines = []
    # if each slot in the pattern is the same, add their payout
    for line_key in money_lines:
        line = money_lines[line_key]
        if line[0] == line[1] == line[2]:
            symbol = line[0]
            multiplier = payouts[symbol]
            payout += multiplier * bet
            winning_lines.append(line_key)
    out = {'board': slots, 'payout': payout, 'winning lines': winning_lines}
    return out

def set_symbols(slots, key="basic"):
    # In: slots matrix & symbol key
    # Out: new matrix with symbols inserted
    out_slots = np.empty((3, 3), dtype=object)
    if key in symbol_map:
        symbols = symbol_map[key]
    else:
        symbols = symbol_map["basic"]
    for y in range(0, 3):
        for x in range(0, 3):
            out_slots[y][x] = symbols[slots[y][x]]
    return out_slots


def test_slots_single(bet : int):
    result = play_slots(bet)
    print(str(result['board']) + "\n\npayout: " + str(result['payout']))

def test_slots_symbols():
    result = play_slots(1)
    for key in symbol_map:
        symbol_slots = set_symbols(result['board'], key)
        print(str(symbol_slots) + '\n-------')


def test_slots_many(sims : int, bet : int):
    # HouseProfit = 0
    player_profit = 0
    house_wins = 0
    # input={'name':'Superice', 'symbols':'cse', 'bet':bet}
    for x in range(sims):
        result = play_slots(bet)
        if result['payout'] <= 0:
            house_wins += 1

        # HouseProfit += result['house']
        player_profit += result['payout'] - bet
    edge = -player_profit / (bet * sims)
    print('Sims ran: ' + str(sims))
    print('Bet per sim: ' + str(bet))
    # print('HouseProfit: '+str(HouseProfit))
    print('Player profit: ' + str(player_profit))
    print('House win rate: ' + str(house_wins / sims))
    print('House edge: ' + str(edge))

if __name__ == '__main__':
    test_slots_single(50)
    print("--------------------------------")
    test_slots_symbols()
    print("--------------------------------")
    test_slots_many(100000, 50)

        

