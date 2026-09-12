import json
import requests

#To-do: check for game differences, auto-return both fusion versions, figure out the weakness chart algorithm
pokemon = input("whats pokemon? ")


def get_id(pokemon):
    with open("pokemon_data.json","r") as pdj:
        dexdata = json.load(pdj)
        for data in dexdata:
            if data['name'].lower() == pokemon:
                id = data['id']
    return id


def get_species(pokemon):
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}").json()
    return r['name']

def get_abilities(pokemon):
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}").json()
    regular_abilities = [
        entry['ability']['name']
        for entry in r['abilities']
        if not entry['is_hidden']
    ]
    hidden_abilities = [
        entry['ability']['name']
        for entry in r['abilities']
        if entry['is_hidden']
    ]

    return (
        regular_abilities[0] if len(regular_abilities) > 0 else None,
        regular_abilities[1] if len(regular_abilities) > 1 else None,
        hidden_abilities[0] if hidden_abilities else None,
    )

def get_level_moves(pokemon):
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}").json()
    movetotal = []
    for move in r['moves']:
        for version in move['version_group_details']:
            if (version['version_group']['name'] != "black-2-white-2" or
                    version['move_learn_method']['name'] != "level-up"):
                continue

            move_name = move['move']['name']
            movedet = requests.get(f"https://pokeapi.co/api/v2/move/{move_name}").json()
            if movedet['accuracy'] is None and movedet['power'] is None:
                move_info = f"Non-damaging | accuracy: 100 | pp: {movedet['pp']} | Type: {movedet['type']['name']}"
            elif movedet['power'] is None and movedet['accuracy'] is not None:
                move_info = f"Non-damaging | accuracy: {movedet['accuracy']} | pp:{movedet['pp']} | Type: {movedet['type']['name']}"
            elif movedet['accuracy'] is None and movedet['power'] is not None:
                move_info = f"Power: {movedet['power']} | accuracy: 100 | pp:{movedet['pp']} | Damage Type: {movedet['damage_class']['name']} | Type: {movedet['type']['name']}"
            else:
                move_info = f"Power: {movedet['power']} | accuracy: {movedet['accuracy']} | pp: {movedet['pp']} | Damage Type: {movedet['damage_class']['name']} | Type: {movedet['type']['name']}"

            movetotal.append(
                f"{move_name}: learned at level {version['level_learned_at']}: {move_info}"
            )
    return movetotal

def get_egg_moves(pokemon):
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}").json()
    re = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon}").json()
    evo = requests.get(re['evolution_chain']['url']).json()
    movetotal = []
    for move in r['moves']:
        for version in move['version_group_details']:
            if (version['version_group']['name'] != "black-2-white-2" or
                    version['move_learn_method']['name'] != "egg"):
                continue

            move_name = move['move']['name']
            movedet = requests.get(f"https://pokeapi.co/api/v2/move/{move_name}").json()
            if movedet['accuracy'] is None and movedet['power'] is None:
                move_info = f"Non-damaging | accuracy: 100 | pp: {movedet['pp']} | Type: {movedet['type']['name']}"
            elif movedet['power'] is None and movedet['accuracy'] is not None:
                move_info = f"Non-damaging | accuracy: {movedet['accuracy']} | pp:{movedet['pp']} | Type: {movedet['type']['name']}"
            elif movedet['accuracy'] is None and movedet['power'] is not None:
                move_info = f"Power: {movedet['power']} | accuracy: 100 | pp:{movedet['pp']} | Damage Type: {movedet['damage_class']['name']} | Type: {movedet['type']['name']}"
            else:
                move_info = f"Power: {movedet['power']} | accuracy: {movedet['accuracy']} | pp: {movedet['pp']} | Damage Type: {movedet['damage_class']['name']} | Type: {movedet['type']['name']}"

            movetotal.append(
                f"{move_name}: learned at level {version['level_learned_at']}: {move_info}"
            )
    return movetotal

def get_tm_moves(pokemon):
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}").json()
    re = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon}").json()
    evo = requests.get(re['evolution_chain']['url']).json()
    movetotal = []
    for move in r['moves']:
        for version in move['version_group_details']:
            if (version['version_group']['name'] != "black-2-white-2" or
                    version['move_learn_method']['name'] != "machine"):
                continue

            move_name = move['move']['name']
            movedet = requests.get(f"https://pokeapi.co/api/v2/move/{move_name}").json()
            if movedet['accuracy'] is None and movedet['power'] is None:
                move_info = f"Non-damaging | accuracy: 100 | pp: {movedet['pp']} | Type: {movedet['type']['name']}"
            elif movedet['power'] is None and movedet['accuracy'] is not None:
                move_info = f"Non-damaging | accuracy: {movedet['accuracy']} | pp:{movedet['pp']} | Type: {movedet['type']['name']}"
            elif movedet['accuracy'] is None and movedet['power'] is not None:
                move_info = f"Power: {movedet['power']} | accuracy: 100 | pp:{movedet['pp']} | Damage Type: {movedet['damage_class']['name']} | Type: {movedet['type']['name']}"
            else:
                move_info = f"Power: {movedet['power']} | accuracy: {movedet['accuracy']} | pp: {movedet['pp']} | Damage Type: {movedet['damage_class']['name']} | Type: {movedet['type']['name']}"

            movetotal.append(
                f"{move_name}: learned at level {version['level_learned_at']}: {move_info}"
            )
    return movetotal
    

def get_types(pokemon):
    with open("pokemon_data.json","r") as pdj:
        dexdata = json.load(pdj)
        for data in dexdata:
            if data['name'].lower() == pokemon:
                types = tuple(type_data['name'] for type_data in data['types'])
                return types[0], types[1] if len(types) > 1 else None

    raise ValueError(f"Unknown Pokemon: {pokemon}")
    
def get_bst(pokemon):

    r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}").json()
    re = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon}").json()
    evo = requests.get(re['evolution_chain']['url']).json()
    hp = r['stats'][0]['base_stat']
    attack = r['stats'][1]['base_stat']
    defense = r['stats'][2]['base_stat']
    special_attack = r['stats'][3]['base_stat']
    special_defense = r['stats'][4]['base_stat']
    speed = r['stats'][5]['base_stat']
    statdict = {"HP": f"{hp}", "ATTACK": f"{attack}", "DEFENSE": f"{defense}", "SPECIAL_ATTACK": f"{special_attack}", "SPECIAL_DEFENSE": f"{special_defense}", "SPEED": f"{speed}"}
    return statdict

def get_evos(pokemon):
    with open("pokemon_data.json", "r") as pdj:
        mons = json.load(pdj)

    for mon in mons:
        if mon["name"].lower() == pokemon.lower():
            evolution = mon.get("evolution", {})

            previous = evolution.get("evolves_from")
            next_evolutions = evolution.get("evolves_to", [])

            return {"previous": previous["name"] if previous else None,
                    "next": [{
            "name": evo["name"],
            "trigger": evo.get("trigger"),
            "level": evo.get("min_level"),
            "condition": evo.get("condition"),
            "item": evo.get("item"),
            "location": evo.get("location"),
            }
            for evo in next_evolutions],}

    raise ValueError(f"Unknown Pokemon: {pokemon}")

if __name__ == "__main__":
    print(get_abilities(pokemon))