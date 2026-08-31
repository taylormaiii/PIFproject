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
