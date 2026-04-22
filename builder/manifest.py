import json
import os
import hashlib
from datetime import datetime

IMAGES_DIR = "/home/nithin/.docksmith/images"


def save_manifest(name, tag, layers, cmd=None, workdir="/", env=None):

    if env is None:
        env = []

    digest_input = "".join([l["digest"] for l in layers])
    digest = hashlib.sha256(digest_input.encode()).hexdigest()

    manifest = {
        "name": name,
        "tag": tag,
        "digest": "sha256:" + digest,
        "created": datetime.utcnow().isoformat(),
        "config": {
            "Env": env,
            "Cmd": cmd,
            "WorkingDir": workdir
        },
        "layers": layers
    }

    path = f"{IMAGES_DIR}/{name}_{tag}.json"

    with open(path, "w") as f:
        json.dump(manifest, f, indent=2)
