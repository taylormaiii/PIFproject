import pokeapitest

def get_body_number_from_symbol(id):
  return id


def get_head_number_from_symbol(id):
  return id


def get_body_species():
  return body_pokemon.id_number


def get_head_species():
  return head_pokemon.id_number


def get_body_species_symbol():
  return body_pokemon.id


def get_head_species_symbol():
  return head_pokemon.id


def adjust_stats_with_evs():
  GameData::Stat.each_main do |s|
  base_stats[s.id] = 1 if not base_stats[s.id] || base_stats[s.id] <= 0
  evs[s.id] = 0 if not evs[s.id] || evs[s.id] < 0
 


#FUSION CALCULATIONS
def calculate_dex_number():
  return (body_pokemon.id_number * NB_POKEMON) + head_pokemon.id_number


def calculate_type1():
  if head_pokemon.type1 == NORMAL & head_pokemon.type2 == FLYING:
    return head_pokemon.type2 
  return head_pokemon.type1


def calculate_type2():
  if body_pokemon.type2 == type1:
    return body_pokemon.type1 
  return body_pokemon.type2


def calculate_base_stats():
  head_stats = head_pokemon.base_stats
  body_stats = body_pokemon.base_stats

  fused_stats = {}

  #Head dominant stats
  fused_stats[:HP] = calculate_fused_stats(head_stats[:HP], body_stats[:HP])
  fused_stats[:SPECIAL_DEFENSE] = calculate_fused_stats(head_stats[:SPECIAL_DEFENSE], body_stats[:SPECIAL_DEFENSE])
  fused_stats[:SPECIAL_ATTACK] = calculate_fused_stats(head_stats[:SPECIAL_ATTACK], body_stats[:SPECIAL_ATTACK])

  #Body dominant stats
  fused_stats[:ATTACK] = calculate_fused_stats(body_stats[:ATTACK], head_stats[:ATTACK])
  fused_stats[:DEFENSE] = calculate_fused_stats(body_stats[:DEFENSE], head_stats[:DEFENSE])
  fused_stats[:SPEED] = calculate_fused_stats(body_stats[:SPEED], head_stats[:SPEED])

  return fused_stats


def calculate_moveset():
  return combine_arrays(body_pokemon.moves, head_pokemon.moves)


def calculate_egg_moves():
  return combine_arrays(body_pokemon.egg_moves, head_pokemon.egg_moves)


def calculate_tutor_moves():
  return combine_arrays(body_pokemon.tutor_moves, head_pokemon.tutor_moves)




def calculate_abilities():
  abilities_hash = []

  ability1 = body_pokemon.abilities[0]
  ability2 = head_pokemon.abilities[0]
  abilities_hash << ability1
  abilities_hash << ability2
  return abilities_hash

def calculate_hidden_abilities():
  abilities_hash = []

  #First two spots are the other abilities of the two pokemon
  ability1 = body_pokemon.abilities[1]
  ability2 = head_pokemon.abilities[1]
  if not ability1:
    ability1 = body_pokemon.abilities[0]
  if not ability2: 
    ability2 = head_pokemon.abilities[0] 

  abilities_hash << ability1
  abilities_hash << ability2

  #add the hidden ability for the two base pokemon
  hiddenAbility1 = body_pokemon.hidden_abilities[0]
  if not hiddenAbility1:
    hiddenAbility1 = ability1 

  hiddenAbility2 = head_pokemon.hidden_abilities[0]
  if  not hiddenAbility2:
    hiddenAbility2 = ability2 

  abilities_hash << hiddenAbility1
  abilities_hash << hiddenAbility2
  return abilities_hash


def calculate_name():
  body_nat_dex = GameData::NAT_DEX_MAPPING[body_pokemon.id_number] ? GameData::NAT_DEX_MAPPING[body_pokemon.id_number] : body_pokemon.id_number
  head_nat_dex = GameData::NAT_DEX_MAPPING[head_pokemon.id_number] ? GameData::NAT_DEX_MAPPING[head_pokemon.id_number] : head_pokemon.id_number
  prefix = GameData::SPLIT_NAMES[head_nat_dex][0]
  suffix = GameData::SPLIT_NAMES[body_nat_dex][1]
  if prefix[-1] == suffix[0]:
    prefix = prefix[0..-2]
    
  return prefix + suffix

def calculate_evolutions():
  body_evolutions = body_pokemon.evolutions
  head_evolutions = head_pokemon.evolutions

  fused_evolutions = []

  #body
  for evolution in body_evolutions:
    evolutionSpecies = evolution[0]
    evolutionSpecies_dex = GameData::Species.get(evolutionSpecies).id_number
    fused_species = _INTL("B{1}H{2}", evolutionSpecies_dex, head_pokemon.id_number)
    fused_evolutions << build_evolution_array(evolution, fused_species)
  

  #head
  for evolution in head_evolutions:
    evolutionSpecies = evolution[0]
    evolutionSpecies_dex = GameData::Species.get(evolutionSpecies).id_number
    fused_species = _INTL("B{1}H{2}", body_pokemon.id_number, evolutionSpecies_dex)
    fused_evolutions << build_evolution_array(evolution, fused_species)
  

  return fused_evolutions


#Change the evolution species deping if head & body and keep the rest of the data the same
def build_evolution_array(evolution_data, new_species):
  fused_evolution_array = []
  fused_evolution_array << new_species.to_sym

  #add the rest
  for data in evolution_data:
    if evolution_data.index(data) == 0:
      fused_evolution_array << data
  
  return fused_evolution_array


def calculate_category():
  return split_and_combine_text(body_pokemon.category, head_pokemon.category, " ")


#############################  UTIL METHODS ###############################

#Takes 2 strings, splits and combines them using the beginning of the first one and the  of the second one
# (for example for pokedex entries)
def split_and_combine_text(beginingText_full, Text_full, separator):
  beginingText_split = beginingText_full.split(separator, 2)
  Text_split = Text_full.split(separator, 2)

  beginningText = beginingText_split[0]
  Text = Text_split[1] & Text_split[1] != "" ? Text_split[1] : Text_split[0]
  return beginningText + separator + " " + Text

def calculate_fused_stats(dominantStat, otherStat):
  return ((2 * dominantStat) / 3) + (otherStat / 3).floor


def average_values(value1, value2):
  return ((value1 + value2) / 2).floor


def average_map_values(map1, map2):
  averaged_map = map1.merge(map2) do |key, value1, value2|
  ((value1 + value2) / 2.0).floor

  return averaged_map


def get_highest_value(value1, value2):
  return value1 > value2 ? value1 : value2


def get_lowest_value(value1, value2):
  return value1 < value2 ? value1 : value2


def combine_arrays(array1, array2):
  return array1 + array2

def initialize(id):
  if id.is_a?(Integer):
    body_id = getBodyID(id)
    head_id = getHeadID(id, body_id)
    pokemon_id = getFusedPokemonIdFromDexNum(body_id, head_id)
    return GameData_FusedSpecies.new(pokemon_id)

  head_id = get_head_number_from_symbol(id)
  body_id = get_body_number_from_symbol(id)

  body_pokemon = GameData_Species.get(body_id)
  head_pokemon = GameData_Species.get(head_id)

  id = id
  id_number = calculate_dex_number()
  species = id
  form = 0
  real_name = calculate_name()
  real_form_name = nil

  type1 = calculate_type1()
  type2 = calculate_type2()

  #Stats
  base_stats = calculate_base_stats()
  evs = calculate_evs()
  adjust_stats_with_evs()

  base_exp = calculate_base_exp()
  growth_rate = calculate_growth_rate()
  ger_ratio = calculate_ger() #todo
  catch_rate = calculate_catch_rate()
  happiness = calculate_base_happiness()

  #Moves
  moves = calculate_moveset()
  tutor_moves = calculate_tutor_moves() # hash[:tutor_moves] || []
  egg_moves = calculate_egg_moves() # hash[:egg_moves] || []

  #Abilities
  abilities = calculate_abilities() # hash[:abilities] || []
  hidden_abilities = calculate_hidden_abilities() # hash[:hidden_abilities] || []



  evolutions = calculate_evolutions() # hash[:evolutions] || []

  #pokedex
  pokedex_form = form #ignored
  real_category = calculate_category()
  real_pokedex_entry = calculate_dex_entry()
  height = average_values(head_pokemon.height, body_pokemon.height)
  weight = average_values(head_pokemon.weight, body_pokemon.weight)
  color = head_pokemon.color
  shape = body_pokemon.shape

  #sprite positioning
  back_sprite_x = body_pokemon.back_sprite_x
  back_sprite_y = body_pokemon.back_sprite_y
  front_sprite_x = body_pokemon.front_sprite_x
  front_sprite_y = body_pokemon.front_sprite_y
  front_sprite_altitude = body_pokemon.front_sprite_altitude
  shadow_x = body_pokemon.shadow_x
  shadow_size = body_pokemon.shadow_size