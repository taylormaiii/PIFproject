try:
  from . import poke_api
except ImportError:
  import poke_api
import requests

#FUSION CALCULATIONS

def calculate_id(head_pokemon, body_pokemon):
  id1 = poke_api.get_id(head_pokemon)
  id2 = poke_api.get_id(body_pokemon)
  return f"{id1}.{id2}"

def calculate_type1(head_pokemon, body_pokemon):
  head_type1, _ = poke_api.get_types(head_pokemon)
  return head_type1

def calculate_type2(head_pokemon, body_pokemon):
  head_type1, _ = poke_api.get_types(head_pokemon)
  body_type1, body_type2 = poke_api.get_types(body_pokemon)

  if body_type2 == head_type1:
    body_type2 = body_type1
  elif body_type2 is None:
    body_type2 = body_type1

  return None if body_type2 == head_type1 else body_type2

def calculate_base_stats(head_pokemon, body_pokemon):
  head_stats = poke_api.get_bst(head_pokemon)
  body_stats = poke_api.get_bst(body_pokemon)
#compare head/body vs fused stats
  fused_stats = {}


  fused_stats['HP'] = calculate_fused_stats(int(head_stats['HP']), int(body_stats['HP']))
  fused_stats['ATTACK'] = calculate_fused_stats(int(body_stats['ATTACK']), int(head_stats['ATTACK']))
  fused_stats['DEFENSE'] = calculate_fused_stats(int(body_stats['DEFENSE']), int(head_stats['DEFENSE']))
  fused_stats['SPECIAL_ATTACK'] = calculate_fused_stats(int(head_stats['SPECIAL_ATTACK']), int(body_stats['SPECIAL_ATTACK']))
  fused_stats['SPECIAL_DEFENSE'] = calculate_fused_stats(int(head_stats['SPECIAL_DEFENSE']), int(body_stats['SPECIAL_DEFENSE']))
  fused_stats['SPEED'] = calculate_fused_stats(int(body_stats['SPEED']), int(head_stats['SPEED']))
  fused_stats['TOTAL'] = fused_stats['HP'] + fused_stats['ATTACK'] + fused_stats['DEFENSE'] + fused_stats['SPECIAL_ATTACK'] + fused_stats['SPECIAL_DEFENSE'] + fused_stats['SPEED']
  return fused_stats

def calculate_moveset(head_pokemon, body_pokemon):
  return combine_list(poke_api.get_level_moves(head_pokemon), poke_api.get_level_moves(body_pokemon))

def calculate_egg_moves(head_pokemon, body_pokemon):
  return combine_list(poke_api.get_egg_moves(head_pokemon), poke_api.get_egg_moves(body_pokemon))

def calculate_tm_moves(head_pokemon, body_pokemon):
  return combine_list(poke_api.get_tm_moves(head_pokemon), poke_api.get_tm_moves(body_pokemon))

def calculate_abilities(head_pokemon, body_pokemon):
  abilities_hash = []

  headability1 = poke_api.get_abilities(head_pokemon)[0]
  headability2 = poke_api.get_abilities(head_pokemon)[1]
  bodyability1 = poke_api.get_abilities(body_pokemon)[0]
  bodyability2 = poke_api.get_abilities(body_pokemon)[1]
  abilities_hash.append(headability1)
  abilities_hash.append(headability2)
  abilities_hash.append(bodyability1)
  abilities_hash.append(bodyability2)
  return abilities_hash

def calculate_hidden_abilities(head_pokemon, body_pokemon):
  hidden_abilities_hash = []

  #First two spots are the other abilities of the two pokemon
  ability1 = poke_api.get_abilities(head_pokemon)[2]
  ability2 = poke_api.get_abilities(body_pokemon)[2]
  if not ability1:
    ability1 = poke_api.get_abilities(body_pokemon)[2]
  if not ability2: 
    ability2 = poke_api.get_abilities(head_pokemon)[2] 

  hidden_abilities_hash.append(ability1)
  hidden_abilities_hash.append(ability2)
  return hidden_abilities_hash

def calculate_evolutions(head_pokemon, body_pokemon):
  body_evolutions = poke_api.get_evos(body_pokemon)
  head_evolutions = poke_api.get_evos(head_pokemon)

  fused_evolutions = []

  #body
  for evolution in body_evolutions["next"]:
    fused_evolutions.append(evolution)
  
  #head
  for evolution in head_evolutions["next"]:
    fused_evolutions.append(evolution)
  
  return fused_evolutions

def get_types(pokemon):
    response = requests.get(
        f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
    ).json()

    types = tuple(
        entry["type"]["name"]
        for entry in response["types"]
    )

    if len(types) == 1:
        return types[0], None

    return types[0], types[1]


#############################  UTIL METHODS ###############################

def calculate_fused_stats(dominantStat, otherStat):
  return (2 * dominantStat + otherStat) // 3

def average_values(value1, value2):
  return ((value1 + value2) // 2)

def get_highest_value(value1, value2):
  return max(value1,value2)

def get_lowest_value(value1, value2):
  return min(value1, value2)

def combine_list(list1, list2):
  return list1 + list2



def return_types(type1, type2):
  return [
        pokemon_type
        for pokemon_type in (type1, type2)
        if pokemon_type is not None
    ]



if __name__ == "__main__":
  head_pokemon = input("Head pokemon ")
  body_pokemon = input("Body pokemon ")

  id = calculate_id(head_pokemon, body_pokemon)
  type1 = calculate_type1(head_pokemon, body_pokemon)
  type2 = calculate_type2(head_pokemon, body_pokemon)
  sprite = f"https://ifd-spaces.sfo2.cdn.digitaloceanspaces.com/custom/{id}.png"

  #find a way to show stat loss + gain vs other option
  base_stats = calculate_base_stats(head_pokemon, body_pokemon)
  moves = calculate_moveset(head_pokemon, body_pokemon)
  tm_moves = calculate_tm_moves(head_pokemon, body_pokemon) # hash[:tutor_moves] || []
  egg_moves = calculate_egg_moves(head_pokemon, body_pokemon) # hash[:egg_moves] || []
  abilities = calculate_abilities(head_pokemon, body_pokemon) # hash[:abilities] || []
  hidden_abilities = calculate_hidden_abilities(head_pokemon, body_pokemon) # hash[:hidden_abilities] || []

  evolutions = calculate_evolutions(head_pokemon, body_pokemon) # hash[:evolutions] || []
  types = return_types(type1,type2)

#automatically show both options
#add a weakness chart
#checker for custom abilities in pif
def calculate_fusion(head_pokemon, body_pokemon):
  return {
    "id": calculate_id(head_pokemon, body_pokemon),
    "head": head_pokemon,
    "body": body_pokemon,
    "sprite": f"https://ifd-spaces.sfo2.cdn.digitaloceanspaces.com/custom/{id}.png",
    "types": return_types(
    calculate_type1(head_pokemon, body_pokemon),
    calculate_type2(head_pokemon, body_pokemon),),
    "stats": calculate_base_stats(head_pokemon, body_pokemon),
    "abilities": calculate_abilities(head_pokemon, body_pokemon),
    "hidden abilities": calculate_hidden_abilities(head_pokemon, body_pokemon),
    "moves": {
        "level": calculate_moveset(head_pokemon, body_pokemon),
        "tm": calculate_tm_moves(head_pokemon, body_pokemon),
        "egg": calculate_egg_moves(head_pokemon, body_pokemon)
    },
    "evolutions": calculate_evolutions(head_pokemon, body_pokemon)
}
