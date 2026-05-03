import json
import os

CONFIG_FILE = "config.json"


def default_config():
    return {
        "indoor": [],
        "outdoor": [],
        "flag": []
    }


def load():
    if not os.path.exists(CONFIG_FILE):
        save([], [], [])
        return default_config()

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()

            if not content:
                save([], [], [])
                return default_config()

            data =  json.loads(content)

            if "flag" not in data:
                data["flag"] = []


            return data


    except json.JSONDecodeError:
        save([], [])
        return default_config()


def save(indoor, outdoor):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "indoor": indoor,
            "outdoor": outdoor,
            "flag": flag
        }, f, ensure_ascii=False, indent=4)