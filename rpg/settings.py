import json
import os.path

SETTINGS_FILE = os.path.normpath(
        os.path.abspath(__file__) + "/../settings.json")

settings = json.load(open(SETTINGS_FILE))
