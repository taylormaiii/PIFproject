import requests
import json
from flask import Flask, render_template, request, make_response, jsonify
import fusion.FusedSpecies as fs
import itertools

app = Flask(__name__)

with open("data/locations.json", encoding="utf-8") as locations_file:
    locations = json.load(locations_file)

with open("data/pokemon_data.json", encoding="utf-8") as pokemon_file:
    pokemon_data = json.load(pokemon_file)

@app.route("/", methods=['GET', 'POST'])
def fusion():
    if request.method == 'POST':
        pokemoncaught = request.form.getlist("caughtmon")
        originals = enumerate(pokemoncaught)
        include_evolutions = request.form.get("include_evolutions") == "true"

        if include_evolutions:
            candidates = add_future_evolutions(originals)
        else:
            candidates = originals
        pokelist = list(combinations(candidates, 2))

        result = []

        for (head_id, head), (body_id, body) in pokelist:
            if head_id == body_id:
                continue

            result.append({
                "pair": [head, body],
                "variants": [
                    fs.calculate_fusion_summary(head, body),
                    fs.calculate_fusion_summary(body, head),
                ],
            })

        return jsonify({"results": result})

    return render_template("base.html",locations=locations,pokemon_data=pokemon_data)


def add_future_evolutions(originals):
    candidates = []

    for instance_id, pokemon_name in originals:
        candidates.append((instance_id, pokemon_name))
        visited = set()
        collect_evolutions(pokemon_name, instance_id, candidates, visited)

    return candidates


def collect_evolutions(pokemon_name, instance_id, candidates, visited):
    if pokemon_name in visited:
        return

    visited.add(pokemon_name)

    evolutions = fs.poke_api.get_evos(pokemon_name)


    for evolution in evolutions["next"]:
        evolution_name = evolution["name"].title()
        candidate = (instance_id, evolution_name)

        if candidate not in candidates:
            candidates.append(candidate)

        collect_evolutions(evolution_name, instance_id, candidates, visited)


def combinations(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))

    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)

@app.route("/api/fusion-details", methods=['POST'])
def fusion_details():
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "invalid json error"}), 400
        head = data["head"]
        body = data["body"]
        if not head or not body:
            return jsonify({"error": "missing head or body"}), 400
        result = []
        result.append({
                    "pair": [head, body],
                    "variants": [
                        fs.calculate_fusion_details(head, body),
                        fs.calculate_fusion_details(body, head),
                    ],
                })

        return jsonify(result)


