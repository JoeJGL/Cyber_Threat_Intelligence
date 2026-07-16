import json

# Fichier d'entrée et de sortie
input_file = "Intrusion_Set.json"
output_file = "threat_actors.json"

# Charger le JSON
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

objects = data.get("objects", [])

names = []
for item in objects:
    if "name" in item:
        names.append(item["name"])

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(names, f, ensure_ascii=False, indent=2)