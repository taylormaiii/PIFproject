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

        include_evolutions = request.form.get("include_evolutions") == "true"

        if include_evolutions:
            pokemoncaught = add_future_evolutions(pokemoncaught)

        pokelist = list(combinations(pokemoncaught, 2))

        result = []

        for head, body in pokelist:
            result.append({
                "pair": [head, body],
                "variants": [
                    fs.calculate_fusion_summary(head, body),
                    fs.calculate_fusion_summary(body, head),
                ],
            })

        return jsonify({"results": result})

    return render_template("base.html",locations=locations,pokemon_data=pokemon_data)


def add_future_evolutions(pokemon_list):
    expanded = list(pokemon_list)
    visited = set()

    for pokemon in pokemon_list:
        collect_evolutions(pokemon, expanded, visited)

    return expanded


def collect_evolutions(pokemon, expanded, visited):
    if pokemon in visited:
        return

    visited.add(pokemon)

    evolutions = fs.poke_api.get_evos(pokemon)

    for evolution in evolutions["next"]:
        evolution_name = evolution["name"]

        if evolution_name not in expanded:
            expanded.append(evolution_name)

        collect_evolutions(evolution_name, expanded, visited)

#find a way to make it so pokemon are not fused with the ones in their own evo group if they are not duplicates


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

@app.route("/api/fusion-details", methods=["POST"])
def fusion_details():
    data = request.get_json()

    result = fs.calculate_fusion_details(
        data["head"],
        data["body"],
    )

    return jsonify(result)


