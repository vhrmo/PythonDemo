import json5

with open("../Data/Servers.json5", 'r') as f:  # open in readonly mode
    servers = json5.load(f)["Servers"]


