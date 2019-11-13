import os
import json

path_to_config = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..',
    'config.json'
)

with open(path_to_config) as json_file:
    config = json.load(json_file)
