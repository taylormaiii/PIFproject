import json

with open("locations.json") as lnif, open("customlocations.json") as clf:
    locations = json.load(lnif)
    custom_locations = json.load(clf)
    location_names = { 
        location["id"]: location["name"] for location in locations
    }

    for entry in custom_locations["playthrough"]["customLocations"]:
        insert_id = entry.get("region", {})
        if insert_id in location_names:
            entry["region"] = location_names[insert_id]
        print(entry["region"])

    with open("customlocations.json", "w") as custom_file:
       json.dump(custom_locations, custom_file, indent=2)
       custom_file.write("\n")