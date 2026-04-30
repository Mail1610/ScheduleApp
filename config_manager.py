import json
import os

CONFIG_FILE = "config.json"


def default_config():
    return {
        "indoor": [],
        "outdoor": []
    }


def load():
    if not os.path.exists(CONFIG_FILE):
        save([], [])
        return default_config()

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()

            if not content:
                save([], [])
                return default_config()

            return json.loads(content)

    except json.JSONDecodeError:
        save([], [])
        return default_config()


def save(indoor, outdoor):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "indoor": indoor,
            "outdoor": outdoor
        }, f, ensure_ascii=False, indent=4)