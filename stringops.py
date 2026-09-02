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
        j = json.load(jf)

        partymonroute = []
        party = j[":player"]["attributes"]["@party"]
        for mon in party:
            for name, route, hatched_map in mon_name_routeinfo(mon):
                if hatched_map != 0:
                    route = f"{route} Egg"
                partymonroute.append(f"{name}: {route}")
        print(partymonroute)

        

def extract_box_route():
    with open("output.json") as jf:
        j = json.load(jf)

        boxmonroute = []

        boxes = j[":storage_system"]["attributes"]["@boxes"]
        for box in boxes:
            if not box:
                continue

            for mon in box["attributes"].get("@pokemon", []):
                if mon is None:
                    continue

                for name, route, hatched_map in mon_name_routeinfo(mon):
                    if hatched_map != 0:
                        route = f"{route} Egg"
                    boxmonroute.append(f"{name}: {route}")

        print(boxmonroute)


def mon_name_routeinfo(mon):
    attrs = mon.get("attributes", {})
    species = attrs.get("@species_data", {})

    if species.get("ruby_class_name") == "GameData::FusedSpecies":
        mon_names = [attrs.get("@original_body"), attrs.get("@original_head")]
    elif species.get("ruby_class_name") == "GameData::Species":
        mon_names = [mon]
    else:
        mon_names = []

    routeinfo = []
    for mon_name in mon_names:
        if not mon_name:
            continue

        mon_name_attrs = mon_name.get("attributes", {})
        mon_name_species = mon_name_attrs.get("@species_data", {})
        name = mon_name_species.get("attributes", {}).get("@id", {}).get("name")
        if name is None:
            continue

        routeinfo.append(
            (
                name,
                mon_name_attrs.get("@obtain_map", attrs.get("@obtain_map")),
                mon_name_attrs.get("@hatched_map", attrs.get("@hatched_map", 0)),
            )
        )

    return routeinfo

extract_box_route()
extract_party_route()