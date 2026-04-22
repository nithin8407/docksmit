import os
import json
import tarfile
import tempfile
import subprocess

BASE_DIR = os.path.expanduser("~/.docksmith")


def run_container(image, env_overrides=None):

    name, tag = image.split(":")

    manifest_path = f"{BASE_DIR}/images/{name}_{tag}.json"

    with open(manifest_path) as f:
        manifest = json.load(f)

    root = tempfile.mkdtemp()

    for layer in manifest["layers"]:
        layer_path = f"{BASE_DIR}/layers/{layer['file']}"
        with tarfile.open(layer_path) as tar:
            tar.extractall(root)

    cmd = manifest["config"]["Cmd"]
    workdir = manifest["config"]["WorkingDir"]
    env = manifest["config"]["Env"]

    env_dict = {}

    for e in env:
        k, v = e.split("=")
        env_dict[k] = v

    if env_overrides:
        for e in env_overrides:
            k, v = e.split("=")
            env_dict[k] = v

    run_env = os.environ.copy()
    run_env.update(env_dict)

    run_path = os.path.join(root, workdir.strip("/"))

    subprocess.run(cmd, cwd=run_path, env=run_env)
