import json
import random
import string
import os
from copy import deepcopy

# ---------- KLASSENDEFINITION ----------
class JsonGenerator:
    def __init__(self, template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            self.template = json.load(f)
        self.current_id = self.template['userData']['id']

    def generate_random_name(self):
        return ''.join(random.choices(string.ascii_uppercase, k=4))

    def apply_rules(self):
        new_data = deepcopy(self.template)

        new_data['userData']['name'] = self.generate_random_name()
        self.current_id += 1
        new_data['userData']['id'] = self.current_id

        qd = new_data['questionaireData']
        qd['answers'] = [random.randint(1, 6) for _ in qd['answers']]

        gd = new_data['gameData']
        gd['times'] = [f"{random.uniform(0, 5):.2f}" for _ in gd['times']]
        gd['results'] = [random.choice([0, 1]) for _ in gd['results']]

        td = new_data['testData']
        td['times'] = [random.randint(1, 5) for _ in td['times']]
        td['answers'] = [random.choice([0, 1]) for _ in td['answers']]
        td['difficulty'] = [random.randint(1, 3) for _ in td['difficulty']]

        self.template = new_data

    def save_new_json(self, output_path):
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.template, f, indent=2)

# ---------- FUNKTION AUSSERHALB DER KLASSE ----------
def generate_multiple_jsons(template_path="data/1.json", output_folder="data", count=300):
    os.makedirs(output_folder, exist_ok=True)
    generator = JsonGenerator(template_path)
    for i in range(count):
        generator.apply_rules()
        generator.save_new_json(f"{output_folder}/_{i+1}.json")

# ---------- EINSTIEGPUNKT ----------
if __name__ == "__main__":
    generate_multiple_jsons()
