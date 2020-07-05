import os
import json

def load(fn='config.txt'):
    if fn not in os.listdir():
        save({}, fn)
    with open(fn) as f:
        config = json.load(f)
    print('config loaded from:', fn)
    return config

def save(config, fn='config.txt'):
    with open(fn, 'w') as f:
        json.dump(config, f, indent=2)
    print('config saved to:', fn)
