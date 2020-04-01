import json

CONFIG_FILE='./config.json'
try:
    with open(CONFIG_FILE) as f:
        global config
        config = json.load(f)
except Exception as e:
    print(e)