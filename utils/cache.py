import os
import hashlib
import json

CACHE_DIR = "/home/nithin/.docksmith/cache"


def compute_cache_key(prev_layer, instruction, workdir, env):

    key_data = {
        "prev_layer": prev_layer,
        "instruction": instruction,
        "workdir": workdir,
        "env": env
    }

    raw = json.dumps(key_data, sort_keys=True)

    return hashlib.sha256(raw.encode()).hexdigest()


def cache_lookup(key):

    path = f"{CACHE_DIR}/{key}.json"

    if os.path.exists(path):

        with open(path) as f:
            data = json.load(f)

        return data["layer"]

    return None


def cache_store(key, layer):

    path = f"{CACHE_DIR}/{key}.json"

    with open(path, "w") as f:

        json.dump({"layer": layer}, f)
