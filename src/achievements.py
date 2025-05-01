from src.database import achievements_db
from src.database import inv_db



achievement_map = {

    'Bankrupt' : {'name' : 'Go Bankrupt', 'Description' : 'Lose all your coins, The House always wins in the end anyway.', 'Task' : 'Hit 0 Coins', 'IncompletePath' : 'public/achievements/BankruptGrey.png', 'CompletePath' : 'public/achievements/BankruptColor.png'},
    'Get Rich' : {'name' : 'Beat The Casino', 'Description' : 'Defy the odds, and show that you are the main character. Beat the house, and claim your treasure.', 'Task' : 'Have 1000 Coins', 'IncompletePath' : 'public/achievements/BeatCasinoGrey.png', 'CompletePath' : 'public/achievements/BeatCasinoColor.png'},
    'Flipper' : {'name' : 'Coin Flip Master', 'Description' : 'Flipping a coin is not all about luck. Show your mastery of the flip, and let everyone know it.', 'Task': 'Win 10 Coin Flips', 'IncompletePath' : 'public/achievements/CFMGrey.png', 'CompletePath' : 'public/achievements/CFMColor.png'},
    'Carousel' : {'name' : 'Roulette Connoisseur', 'Description' : 'Maybe the game about a spinning wheel is not random after all, maybe you can just see the future, and maybe I do not know what I am talking about. Once you have the pallet there is nothing you do not know about this game, perfect the pallet and let the world know it', 'Task' : 'Win 10 games of Roulette', 'IncompletePath' : 'public/achievements/CarouselGrey.png', 'CompletePath' : 'public/achievements/CarouselColor.png'}

}

# Inserts bools for Bankrupt and Get Rich so when they reach the correct number of coins they can be set to true
# Inserts 0 for Glipper and Carousel so we can increment them each time a user wins 

def create_achievements(username):
    data = {'username' : username, 'Bankrupt' : False, 'Get Rich' : False, 'Flipper' : 0, 'Carousel' : 0}
    achievements_db.insert_one(data)

def increment_flipper(username):
    user_data = achievements_db.find_one({'username' : username},{'_id' : 0})
    FlipsWon = user_data['Flipper']
    FlipsWon += 1
    achievements_db.find_one_and_update({'username' : username}, {'$set' : {'Flipper' : FlipsWon}})

def increment_carousel(username):
    user_data = achievements_db.find_one({'username' : username},{'_id' : 0})
    RouletteWon = user_data['Carousel']
    RouletteWon += 1
    achievements_db.find_one_and_update({'username' : username}, {'$set' : {'Carousel' : RouletteWon}})

def set_bankrupt(username):
    user_data = inv_db.find_one({'username' : username}, {'_id' : 0})
    balance = user_data['coins']
    if balance == 0:
        achievements_db.find_one_and_update({'username' : username}, {'$set' : {'Bankrupt' : True}})

def set_get_rich(username):
    user_data = inv_db.find_one({'username' : username}, {'_id' : 0})
    balance = user_data['coins']
    if balance >= 1000:
        achievements_db.find_one_and_update({'username' : username}, {'$set' : {'Get Rich' : True}})

def check_bankrupt(username):
    user_data = inv_db.find_one({'username' : username}, {'_id' : 0})

    if user_data['Bankrupt']:
        return True
    else:
        return False
    
def check_get_rich(username):
    user_data = inv_db.find_one({'username' : username}, {'_id' : 0})
    if user_data['Get Rich']:
        return True
    else: 
        return False

def check_flipper(username):
    user_data = achievements_db.find_one({'username' : username},{'_id' : 0})
    if user_data['Flipper'] >= 10:
        return True
    else:
        return False
    
def check_carousel(username):
    user_data = inv_db.find_one({'username' : username}, {'_id' : 0})
    if user_data['Carousel'] >= 10:
        return True
    else:
        return False
    
def get_all_achivement_pics(username):
    #In: username
    #Out: dict mapping Codnames to Achivement Picture
    out={}

    if check_bankrupt(username):
        out['Bankrupt'] = achievement_map['Bankrupt']['CompletePath']
    else:
        out['Bankrupt'] = achievement_map['Bankrupt']['IncompletePath']

    if check_get_rich(username):
        out['Get Rich'] = achievement_map['Get Rich']['CompletePath']
    else:
        out['Get Rich'] = achievement_map['Get Rich']['IncompletePath']

    if check_flipper(username):
        out['Flipper'] = achievement_map['Flipper']['CompletePath']
    else:
        out['Flipper'] = achievement_map['Flipper']['IncompletePath']

    if check_carousel(username):
        out['Carousel'] = achievement_map['Carousel']['CompletePath']
    else:
        out['Carousel'] = achievement_map['Carousel']['IncompletePath']
    return out

def generate_html_data(username):
    #In: username
    #Out: Dict key = codenames that maps to a dict of achievement name, achievement description, achievement task, and path to photo
    out={}

    paths=get_all_achivement_pics(username)

    for key in paths:
        out[key] = {'name' : achievement_map[key]['name'], 'Description' : achievement_map[key]['Description'], 'Task' : achievement_map[key]['Task'], 'Path' : paths[key]}

    return out


