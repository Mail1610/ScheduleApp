import json
import os

CONFIG_FILE = "config.json"


def default_config():
    return {
        "indoor": [],
        "outdoor": [],
        "no_flag": [],
        "no_morning_outdoor": [],
        "no_so_outdoor": [],
        "no_flag_down": [],
        "no_afternoon_outdoor": [],
        "avoid": []
    }


def load():
    if not os.path.exists(CONFIG_FILE):
        save([], [], [], [], [])
        return default_config()

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()

            if not content:
                save([], [], [], [], [])
                return default_config()

            data = json.loads(content)

            data.setdefault("indoor", [])
            data.setdefault("outdoor", [])
            data.setdefault("no_flag", [])
            data.setdefault("no_morning_outdoor", [])
            data.setdefault("no_so_outdoor", [])
            data.setdefault("no_flag_down", [])
            data.setdefault("no_afternoon_outdoor", [])
            data.setdefault("avoid", [])

            return data

    except json.JSONDecodeError:
        save([], [], [], [], [])
        return default_config()


def save(indoor, outdoor, no_flag, no_morning_outdoor, avoid=None,
         no_flag_down=None, no_afternoon_outdoor=None, no_so_outdoor=None):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "indoor": indoor,
            "outdoor": outdoor,
            "no_flag": no_flag,
            "no_morning_outdoor": no_morning_outdoor,
            "no_so_outdoor": no_so_outdoor or [],
            "no_flag_down": no_flag_down or [],
            "no_afternoon_outdoor": no_afternoon_outdoor or [],
            "avoid": avoid or []
        }, f, ensure_ascii=False, indent=4)