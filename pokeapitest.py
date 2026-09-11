import json
import requests


pokemon = input("whats pokemon? ")
r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}").json()
re = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon}").json()
evo = requests.get(re['evolution_chain']['url']).json()
def get_abilities():
    pokeabilities = [r['abilities'][0]['ability']['name'], r['abilities'][1]['ability']['name']]
    hiddenabilities = r['abilities'][2]['ability']['name']
    return f"Regular Abilities: {pokeabilities}, Hidden Abilities: {hiddenabilities}"

def get_moves():
    moves = []
    learn_level = []
    pairs = []
    pokemoves = r['moves']
    moveinfo = []
    movetotal = []
    for move in pokemoves:
        moves.append(move['move']['name'])
        for version in move['version_group_details']:
            if version['version_group']['name'] == "black-2-white-2":
                learn_level.append(version['level_learned_at'])
        movedet = requests.get(f"https://pokeapi.co/api/v2/move/{move['move']['name']}").json()
        if movedet['accuracy'] is None and movedet['power'] is None:
            moveinfo.append(f"Non-damaging | accuracy: 100 | pp: {movedet['pp']}")            
        elif movedet['power'] is None and movedet['accuracy'] is not None:
            moveinfo.append(f"Non-damaging | accuracy: {movedet['accuracy']} | pp:{movedet['pp']}")
        elif movedet['accuracy'] is None and movedet['power'] is not None:
            moveinfo.append(f"Power: {movedet['power']} | accuracy: 100 | pp:{movedet['pp']}")
        else:
            moveinfo.append(f"Power: {movedet['power']} | accuracy: {movedet['accuracy']} | pp: {movedet['pp']}")
    #add physical/special if power
    for item1, item2 in zip(moves,learn_level):
        pairs.append(f"{item1}: learned at level {item2}")
    for item1, item2 in zip(pairs, moveinfo):
        movetotal.append(f"{item1}: {item2}")
    return movetotal

    

def get_types():
    types = r['types'][0]['type']['name']
    try:
        types1 = r['types'][1]['type']['name']
        return types, types1
    except IndexError:
        return types
    
def get_bst():
    hp = r['stats'][0]['base_stat']
    attack = r['stats'][1]['base_stat']
    defense = r['stats'][2]['base_stat']
    special_attack = r['stats'][3]['base_stat']
    special_defense = r['stats'][4]['base_stat']
    speed = r['stats'][5]['base_stat']
    return f"HP: {hp}, Attack: {attack}, Defense: {defense}, Special Attack: {special_attack}, Special Defense: {special_defense},Speed: {speed}"

def get_evos():
    try:
        evoinfo = [evo['chain']['species']['name'],evo['chain']['evolves_to'][0]['species']['name'],evo['chain']['evolves_to'][0]['evolves_to'][0]['species']['name']]
    except IndexError:
        try:
            evoinfo = [evo['chain']['species']['name'],evo['chain']['evolves_to'][0]['species']['name']]
        except IndexError:
            evoinfo = evo['chain']['species']['name']
    return evoinfo

print(get_moves())