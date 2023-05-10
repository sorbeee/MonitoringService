import json

global config_path
config_path = "config.json"

def read_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def write_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
