import json
import os


def load_cards(filename='cards.json'):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8')as f:
            return json.load(f)
    else:
        return []


def save_cards(data, filename='cards.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)