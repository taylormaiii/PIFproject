import json
from functools import lru_cache
import requests
from pathlib import Path

POKEMON_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "pokemon_data.json"

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

POKEAPI_NAME_OVERRIDES = {
    "oricorio-baile-style": "oricorio-baile",
    "oricorio-pom-pom-style": "oricorio-pom-pom",
    "oricorio-pau-style": "oricorio-pau",
    "oricorio-sensu-style": "oricorio-sensu",
    "meloetta-aria-form": "meloetta-aria",
    "meloetta-pirouette-form": "meloetta-pirouette",
    "lycanroc-midday-form": "lycanroc-midday",
    "lycanroc-midnight-form": "lycanroc-midnight",
    "minior-meteor-form": "minior-blue-meteor",
    "minior-core-form": "minior-blue"
}


@lru_cache(maxsize=None)
def get_pokemon_data(pokemon):
    normalized_pokemon = normalize_pokemon_name(pokemon)
    api_name = POKEAPI_NAME_OVERRIDES.get(normalized_pokemon, normalized_pokemon)
    try:
        re = requests.get(f"https://pokeapi.co/api/v2/pokemon/{api_name}").json()
        species = requests.get(re['species']['url']).json()
        evo = requests.get(species['evolution_chain']['url']).json()
        return re, evo
    except requests.exceptions.ConnectionError as e:
        print(f"{e} : Timed out")

def get_id(pokemon):
    normalized_pokemon = normalize_pokemon_name(pokemon)
    with open(POKEMON_DATA_PATH, "r", encoding="utf-8") as pdj:
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

    abilities = (
        regular_abilities[0].title() if len(regular_abilities) > 0 else None,
        regular_abilities[1].title() if len(regular_abilities) > 1 else None,
        hidden_abilities[0].title() if hidden_abilities else None,
    )
    return check_abilities(pokemon,abilities)

def get_types(pokemon):
    normalized_pokemon = normalize_pokemon_name(pokemon)
    with open(POKEMON_DATA_PATH, "r", encoding="utf-8") as pdj:
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
    with open(POKEMON_DATA_PATH, "r", encoding="utf-8") as pdj:
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

def check_abilities(pokemon,abilities):
    regular1, regular2, hidden = abilities
    name = normalize_pokemon_name(pokemon)

    if name == "talonflame":
        regular1 = "Big Pecks"
    if name == 'gengar':
        regular1 = "Cursed Body"
        hidden = "Levitate"
    if name == "unown":
        hidden = "Mummy"
    if name == "koffing" or name == "weezing":
        hidden = "Stench"
    if name == "flygon":
        hidden = "Dry Skin"
    if name == "regigigas":
        hidden = "Mold Breaker"
    if name == "delibird":
        hidden = "Snow Warning"
    if name == "zapdos":
        hidden = "Lightning Rod"
    if name == "raikou":
        hidden = "Volt Absorb"
    if name == "suicune":
        hidden = "Water Absorb"
    if name == "entei":
        hidden = "Flash Fire"
    if name == "litwick" or name == "lampent" or name == "chandelure":
        hidden = "Shadow Tag"
    if name == "darkrai":
        hidden = "White Smoke"
    if name == "mewtwo":
        hidden = "Immunity"
    if name == "kyurem":
        hidden = "Ice Body"
    if name == "zekrom":
        hidden = "Volt Absorb"
    if name == "reshiram":
        hidden = "Flare Boost"
    if name == "hydreigon":
        hidden = "Hustle"
    if name == "genesect":
        hidden = "Motor Drive"


    return regular1, regular2, hidden