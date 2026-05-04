import json
import os

CONFIG_FILE = "config.json"


def default_config():
    return {
        "indoor": [],
        "outdoor": [],
        "no_flag": [],
        "no_morning_outdoor": []
    }


def load():
    if not os.path.exists(CONFIG_FILE):
        save([], [], [], [])
        return default_config()

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()

            if not content:
                save([], [], [], [])
                return default_config()

            data = json.loads(content)

            data.setdefault("indoor", [])
            data.setdefault("outdoor", [])
            data.setdefault("no_flag", [])
            data.setdefault("no_morning_outdoor", [])

            return data

    except json.JSONDecodeError:
        save([], [], [], [])
        return default_config()


def save(indoor, outdoor, no_flag, no_morning_outdoor):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "indoor": indoor,
            "outdoor": outdoor,
            "no_flag": no_flag,
            "no_morning_outdoor": no_morning_outdoor
        }, f, ensure_ascii=False, indent=4)