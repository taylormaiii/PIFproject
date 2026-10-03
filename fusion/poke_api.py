import json
from functools import lru_cache
import requests

#To-do: check for game differences, figure out the weakness chart algorithm

def normalize_pokemon_name(pokemon):
    normalized = str(pokemon).strip().lower()
    normalized = normalized.replace("♀", "-f")
    normalized = normalized.replace("♂", "-m")
    normalized = normalized.replace("’", "")
    normalized = normalized.replace("'", "")
    normalized = normalized.replace(".", "")
    normalized = normalized.replace(" ", "-")
    normalized = normalized.replace("-", "-")
    return normalized

@lru_cache(maxsize=None)
def get_pokemon_data(pokemon):
    normalized_pokemon = normalize_pokemon_name(pokemon)
    try:
        re = requests.get(f"https://pokeapi.co/api/v2/pokemon/{normalized_pokemon}").json()
        species = requests.get(re['species']['url']).json()
        evo = requests.get(species['evolution_chain']['url']).json()
        return re, evo
    except requests.exceptions.ConnectionError as e:
        print(f"{e} : Timed out")

def get_id(pokemon):
    r, e = get_pokemon_data(pokemon)
    normalized_pokemon = normalize_pokemon_name(pokemon)
    with open(r"data\pokemon_data.json", "r", encoding="utf-8") as pdj:
        dexdata = json.load(pdj)
        for data in dexdata:
            if normalize_pokemon_name(data['name']) == normalized_pokemon:
                id = data['id']
                return id
    raise ValueError(f"Unknown Pokemon: {pokemon}")

def get_evo_id(pokemon):
    r, e = get_pokemon_data(pokemon)
    normalized_pokemon = normalize_pokemon_name(pokemon)
    evo_id = e["id"]
    return evo_id


def get_species(pokemon):
    r,e = get_pokemon_data(pokemon)
    return r['name']

def get_abilities(pokemon):
    r,e = get_pokemon_data(pokemon)
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

def get_types(pokemon):
    normalized_pokemon = normalize_pokemon_name(pokemon)
    with open(r"data\pokemon_data.json", "r", encoding="utf-8") as pdj:
        dexdata = json.load(pdj)
        for data in dexdata:
            if normalize_pokemon_name(data['name']) == normalized_pokemon:
                types = tuple(type_data['name'] for type_data in data['types'])
                return types[0], types[1] if len(types) > 1 else None

    raise ValueError(f"Unknown Pokemon: {pokemon}")
    
def get_bst(pokemon):

    r, e = get_pokemon_data(pokemon)
    hp = r['stats'][0]['base_stat']
    attack = r['stats'][1]['base_stat']
    defense = r['stats'][2]['base_stat']
    special_attack = r['stats'][3]['base_stat']
    special_defense = r['stats'][4]['base_stat']
    speed = r['stats'][5]['base_stat']
    statdict = {"HP": f"{hp}", "ATTACK": f"{attack}", "DEFENSE": f"{defense}", "SPECIAL_ATTACK": f"{special_attack}", "SPECIAL_DEFENSE": f"{special_defense}", "SPEED": f"{speed}"}
    return statdict

def get_evos(pokemon):
    normalized_pokemon = normalize_pokemon_name(pokemon)
    with open(r"data\pokemon_data.json", "r", encoding="utf-8") as pdj:
        mons = json.load(pdj)

    for mon in mons:
        if normalize_pokemon_name(mon["name"]) == normalized_pokemon:
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
