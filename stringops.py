import json

def extract_location():
    with open('outputmap.json') as nf:
        q = json.load(nf)
        names = []
        ids = []
        pairs = []
        for key in q.keys():
            ids.append(key)
        for q_key in q:
            name_attr = q[q_key]['attributes']['@name']
            if isinstance(name_attr, dict):
                q_values = name_attr['text']
            else:
                q_values = name_attr
            names.append(q_values)
        for item1, item2 in zip(ids, names):
            pairs.append(f"{item1}: {item2}")
        return pairs

with open("locationsnamesids.txt", "w") as f:
    for pair in extract_location():
        f.write(pair + "\n")

        mons = []
        routes = []

def extract_party_route():
    with open("output.json") as jf:
        counter = 0
        j = json.load(jf)

        partymonroute = []
        if j["player"]["attributes"]["@party"][counter]["attributes"]["@species_data"]["ruby_class_name"] == "GameData::FusedSpecies":
            while counter < 6:
                monbody = j["player"]["attributes"]["@party"][counter]["attributes"]["@species_data"]["attributes"]["@body_pokemon"]["attributes"]["@id"]["name"]
                monhead = j["player"]["attributes"]["@party"][counter]["attributes"]["@species_data"]["attributes"]["@head_pokemon"]["attributes"]["@id"]["name"]
                routebody = j
                routehead = j
                mons.append(monbody)
                mons.append(monhead)
                counter += 1
        else:
            mon = j[":storage_system"]["attributes"]["@party"][counter]["attributes"]["@species_data"]["attributes"]["@id"]["name"]
            mons.append(mon)

        

def extract_box_route():
    with open("output.json") as jf:
        counter = 0
        j = json.load(jf)

        boxmonroute = []
        box = j[":storage_system"]["attributes"]["@boxes"][counter]
        pokemon_list = box["attributes"]["@pokemon"]
        for mon in pokemon_list:
            if mon is not None:
                species = mon["attributes"]["@species_data"]
                species_type = species.get("ruby_class_name")
                if species_type == "GameData::FusedSpecies":
                    bodyname = species["attributes"]["@body_pokemon"]["attributes"]["@id"]["name"]
                    headname = species["attributes"]["@head_pokemon"]["attributes"]["@id"]["name"]
                    mons.append(bodyname)
                    mons.append(headname)
                elif species_type == "GameData::Species":
                    bodyname = species["attributes"]["@id"]["name"]
                    mons.append(bodyname)
                else:
                    continue
        print(mons)

extract_party_route()
extract_box_route()