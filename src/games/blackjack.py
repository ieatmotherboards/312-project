from random import randint

class Blackjack:

    def __init__(self, bets : dict[str, int]):
        self.deck : list[Card] = create_deck()
        self.bets = bets
        self.players : list[str] = []
        self.hands : dict[str, list[Card]] = {"dealer": []}
        # initializes player hands
        for player in self.bets:
            self.players.append(player)
            self.hands[player] = []

    def dealer_draw(self):
        dealer_hand = self.hands["dealer"]
        while calc_score(dealer_hand) <= 16:
            dealer_hand.append(draw_card(self.deck))

    def deal_players(self):
        for player in self.players:
            hand = self.hands[player]
            hand.append(draw_card(self.deck))
            hand.append(draw_card(self.deck))

    def player_hit(self, player : str):
        hand = self.hands[player]
        hand.append(draw_card(self.deck))
        return hand

    def calc_winnings(self):
        # Returns dict with player's winnings
        scores = {}
        for player in self.hands:
            scores[player] = calc_score(self.hands[player])
        dealer_score = scores['dealer']
        payouts = {}
        for player in self.players:
            player_score = scores[player]
            player_bet = self.bets[player]
            if player_score > 21:
                if dealer_score > 21:
                    # draw
                    payout = player_bet
                else:
                    # player lost
                    payout = 0
            elif dealer_score > 21 or player_score > dealer_score:
                if player_score == 21:
                    # win 1.5x bet
                    payout = player_bet * 2.5
                else:
                    # win bet
                    payout = player_bet * 2
            elif player_score < dealer_score:
                # player lost
                payout = 0
            else:
                # draw
                payout = player_bet
            payouts[player] = float(payout)
        return payouts

# maps card's ranks to their values
value_map : dict[str: int | tuple[int, int]] = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10,
    "Ace": (1, 11)
}

# card object, stores the card's suit, rank, and value.
    # aces have their value stored as a tuple
class Card:
    def __init__(self, suit : str, rank : str):
        self.suit : str = suit
        self.rank : str = rank
        self.value : int | tuple[int, int] = value_map[rank]

    def __str__(self):
        return "'" + self.rank + "' of '" + self.suit + "' [" + str(self.value) + "]"

    def to_id(self):
        return self.rank + "_" + self.suit


def create_deck():
    # Returns a single 52-card deck as a list
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    deck : list[Card] = []
    for suit in suits:
        for rank in ranks:
            deck.append(Card(suit, rank))
    return deck

def draw_card(deck : list[Card]):
    # Returns the card that is drawn
    return deck.pop(randint(0,len(deck)-1))

def calc_score(hand : list[Card]):
    # Returns score of hand
    score = 0
    ace_hold : list[Card] = []
    for card in hand:
        # rank = card.rank
        # suit = card.suit
        value = card.value
        if isinstance(value, tuple):
            ace_hold.append(card)
        else:
            score += value
    ace_count = len(ace_hold)
    # not modular, assumes aces have low of 1 and high of 11 (too much work)
    for _ in ace_hold:
        if ace_count * 11 + score <= 21:
            score += (ace_count * 11)
            break
        else:
            ace_count -= 1
            score += 1
    return score

def test_hand_score():
    hand = [Card("Hearts", "Ace"), Card("Spades", "Ace"), Card("Hearts", "King"), Card("Hearts", "Ace")]
    expected = 13
    actual = calc_score(hand)
    assert expected == actual
    hand.append(Card("Clubs", "2"))
    expected = 15
    actual = calc_score(hand)
    assert expected == actual

def test_game():
    game = Blackjack({"me": 10, "him": 300})
    game.dealer_draw()
    game.deal_players()
    for player in game.players:
        hand = game.hands[player]
        while calc_score(hand) <= 16:
            game.player_hit(player)
    winnings = game.calc_winnings()
    pass

if __name__ == '__main__':
    test_hand_score()
    test_game()


