import pokeapitest
import requests

head_pokemon = input("Head pokemon ")
body_pokemon = input("Body pokemon ")

#FUSION CALCULATIONS

def calculate_id():
  id1 = pokeapitest.get_id(head_pokemon)
  id2 = pokeapitest.get_id(body_pokemon)
  return f"{id1}.{id2}"

def calculate_type1():
  head_type1, _ = pokeapitest.get_types(head_pokemon)
  return head_type1

def calculate_type2():
  head_type1, _ = pokeapitest.get_types(head_pokemon)
  body_type1, body_type2 = pokeapitest.get_types(body_pokemon)

  if body_type2 == head_type1:
    body_type2 = body_type1
  elif body_type2 is None:
    body_type2 = body_type1

  return None if body_type2 == head_type1 else body_type2

def calculate_base_stats():
  head_stats = pokeapitest.get_bst(head_pokemon)
  body_stats = pokeapitest.get_bst(body_pokemon)

  fused_stats = {}


  fused_stats['HP'] = calculate_fused_stats(int(head_stats['HP']), int(body_stats['HP']))
  fused_stats['ATTACK'] = calculate_fused_stats(int(body_stats['ATTACK']), int(head_stats['ATTACK']))
  fused_stats['DEFENSE'] = calculate_fused_stats(int(body_stats['DEFENSE']), int(head_stats['DEFENSE']))
  fused_stats['SPECIAL_ATTACK'] = calculate_fused_stats(int(head_stats['SPECIAL_ATTACK']), int(body_stats['SPECIAL_ATTACK']))
  fused_stats['SPECIAL_DEFENSE'] = calculate_fused_stats(int(head_stats['SPECIAL_DEFENSE']), int(body_stats['SPECIAL_DEFENSE']))
  fused_stats['SPEED'] = calculate_fused_stats(int(body_stats['SPEED']), int(head_stats['SPEED']))
  fused_stats['TOTAL'] = fused_stats['HP'] + fused_stats['ATTACK'] + fused_stats['DEFENSE'] + fused_stats['SPECIAL_ATTACK'] + fused_stats['SPECIAL_DEFENSE'] + fused_stats['SPEED']
  return fused_stats

def calculate_moveset():
  return combine_list(pokeapitest.get_level_moves(head_pokemon), pokeapitest.get_level_moves(body_pokemon))

def calculate_egg_moves():
  return combine_list(pokeapitest.get_egg_moves(head_pokemon), pokeapitest.get_egg_moves(body_pokemon))

def calculate_tm_moves():
  return combine_list(pokeapitest.get_tm_moves(head_pokemon), pokeapitest.get_tm_moves(body_pokemon))

def calculate_abilities():
  abilities_hash = []

  headability1 = pokeapitest.get_abilities(head_pokemon)[0]
  headability2 = pokeapitest.get_abilities(head_pokemon)[1]
  bodyability1 = pokeapitest.get_abilities(body_pokemon)[0]
  bodyability2 = pokeapitest.get_abilities(body_pokemon)[1]
  abilities_hash.append(headability1)
  abilities_hash.append(headability2)
  abilities_hash.append(bodyability1)
  abilities_hash.append(bodyability2)
  return abilities_hash

def calculate_hidden_abilities():
  hidden_abilities_hash = []

  #First two spots are the other abilities of the two pokemon
  ability1 = pokeapitest.get_abilities(head_pokemon)[2]
  ability2 = pokeapitest.get_abilities(body_pokemon)[2]
  if not ability1:
    ability1 = pokeapitest.get_abilities(body_pokemon)[2]
  if not ability2: 
    ability2 = pokeapitest.get_abilities(head_pokemon)[2] 

  hidden_abilities_hash.append(ability1)
  hidden_abilities_hash.append(ability2)
  return hidden_abilities_hash

def calculate_evolutions():
  body_evolutions = pokeapitest.get_evos(body_pokemon)
  head_evolutions = pokeapitest.get_evos(head_pokemon)

  fused_evolutions = []

  #body
  for evolution in body_evolutions:
    fused_evolutions.append(evolution)
  
  #head
  for evolution in head_evolutions:
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
  return zip(list1,list2)

id = calculate_id()
type1 = calculate_type1()
type2 = calculate_type2()

#Stats
#find a way to show stat loss + gain
base_stats = calculate_base_stats()

#Moves
moves = calculate_moveset()
tm_moves = calculate_tm_moves() # hash[:tutor_moves] || []
egg_moves = calculate_egg_moves() # hash[:egg_moves] || []

#Abilities
abilities = calculate_abilities() # hash[:abilities] || []
hidden_abilities = calculate_hidden_abilities() # hash[:hidden_abilities] || []

evolutions = calculate_evolutions() # hash[:evolutions] || []
#automatically show both options
#add a weakness chart
print(id,type1,type2,base_stats,abilities,evolutions)