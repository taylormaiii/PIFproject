import json

with open("output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("output2.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)