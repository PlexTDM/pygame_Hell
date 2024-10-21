from pathlib import Path
import json

path = Path("./save.json")

# onStart
def loadGame():
    data = {"highestScore": 0}
    try:
        with open(path) as load_file:
            data = json.load(load_file)
            return data
    except:
        with open(path, "w") as store_file:
            json.dump(data, store_file)
            return data


def saveGame(score, kills):
    data = {"highestScore": score, "kills":kills}

    with open(path, "w") as store_data:
        json.dump(data, store_data)
        
# stuff?
frame_rate = 60
SC_WIDTH = 1280
SC_HEIGHT = 720

LAYERS = {
    'water':0,
    'ground':1,
    'obstacles':2,
    'ground_effects':3,
    'main':4,
    'enemy':5,
    'air_effects':6,
    'ui':99,
}
TILE_SIZE = 64 #default-32
# IDK WHAT IM DOING
UPGRADES1 = {
    'penetration': {
        "name": "Penetration",
        'description': 'Hits one more enemy'
    },
    'attack': {
        'name': 'Damage UP',
        'description': '+5 attack dmg'
    },
    'attack_speed': {
        'name': 'Faster Attack',
        'description': '+10% attack speed'
    }
}