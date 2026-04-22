import os
import argparse
import tempfile
import json

from builder.parser import parse_docksmithfile
from builder.build_engine import execute_copy, execute_run
from utils.layer import create_layer
from builder.manifest import save_manifest
from runtime.container_runner import run_container
from utils.cache import compute_cache_key, cache_lookup, cache_store

BASE_DIR = os.path.expanduser("~/.docksmith")


def init_storage():
    os.makedirs(BASE_DIR + "/images", exist_ok=True)
    os.makedirs(BASE_DIR + "/layers", exist_ok=True)
    os.makedirs(BASE_DIR + "/cache", exist_ok=True)


def load_base_image(base_name):

    base_manifest = f"{BASE_DIR}/images/{base_name}_latest.json"

    if not os.path.exists(base_manifest):
        print(f"Base image '{base_name}' not found")
        return []

    with open(base_manifest) as f:
        manifest = json.load(f)

    return manifest.get("layers", [])


def main():

    parser = argparse.ArgumentParser()

    sub = parser.add_subparsers(dest="command")

    sub.add_parser("images")

    build = sub.add_parser("build")
    build.add_argument("-t")
    build.add_argument("context")

    run = sub.add_parser("run")
    run.add_argument("-e", "--env", action="append", default=[])
    run.add_argument("image")

    rmi = sub.add_parser("rmi")
    rmi.add_argument("image")

    args = parser.parse_args()

    # ---------------- IMAGES ----------------
    if args.command == "images":

        images_dir = BASE_DIR + "/images"

        files = os.listdir(images_dir)

        if not files:
            print("No images found")
            return

        print(f"{'NAME':<10} {'TAG':<10} {'IMAGE ID':<15} {'CREATED'}")

        for f in files:

            path = os.path.join(images_dir, f)

            with open(path) as mf:
                manifest = json.load(mf)

            name = manifest.get("name", "unknown")
            tag = manifest.get("tag", "latest")

            digest = manifest.get("digest", "base")

            if ":" in digest:
                image_id = digest.split(":")[1][:12]
            else:
                image_id = digest[:12]

            created = manifest.get("created", "unknown")

            print(f"{name:<10} {tag:<10} {image_id:<15} {created}")

    # ---------------- BUILD ----------------
    elif args.command == "build":

        instructions = parse_docksmithfile(args.context)

        print("Parsed instructions:")
        for inst in instructions:
            print(inst)

        build_root = tempfile.mkdtemp()

        layers = []
        cmd = None
        workdir = "/"
        env_vars = []

        prev_layer = None

        for instr, arg in instructions:

            if instr == "FROM":

                base_layers = load_base_image(arg)

                layers.extend(base_layers)

                if base_layers:
                    prev_layer = base_layers[-1]["digest"]

                print(f"Using base image: {arg}")

            elif instr == "COPY":

                key = compute_cache_key(prev_layer, f"COPY {arg}", workdir, env_vars)

                cached = cache_lookup(key)

                if cached:
                    print(f"COPY {arg}  [CACHE HIT]")
                    layers.append(cached)
                    prev_layer = cached["digest"]
                    continue

                print(f"COPY {arg}  [CACHE MISS]")

                src, dest = arg.split()

                execute_copy(src, dest, args.context, build_root)

                layer = create_layer(build_root, f"{instr} {arg}")

                layers.append(layer)

                cache_store(key, layer)

                prev_layer = layer["digest"]

            elif instr == "RUN":

                key = compute_cache_key(prev_layer, f"RUN {arg}", workdir, env_vars)

                cached = cache_lookup(key)

                if cached:
                    print(f"RUN {arg}  [CACHE HIT]")
                    layers.append(cached)
                    prev_layer = cached["digest"]
                    continue

                print(f"RUN {arg}  [CACHE MISS]")

                execute_run(arg, build_root)

                layer = create_layer(build_root, f"{instr} {arg}")

                layers.append(layer)

                cache_store(key, layer)

                prev_layer = layer["digest"]

            elif instr == "CMD":
                cmd = json.loads(arg)

            elif instr == "WORKDIR":
                workdir = arg

            elif instr == "ENV":
                env_vars.append(arg)

        name, tag = args.t.split(":")

        save_manifest(name, tag, layers, cmd, workdir, env_vars)

        print("Image saved:", args.t)

    # ---------------- RUN ----------------
    elif args.command == "run":

        run_container(args.image, args.env)

    # ---------------- REMOVE IMAGE ----------------
    elif args.command == "rmi":

        name, tag = args.image.split(":")

        manifest_path = f"{BASE_DIR}/images/{name}_{tag}.json"

        if os.path.exists(manifest_path):
            os.remove(manifest_path)
            print("Image removed:", args.image)
        else:
            print("Image not found")


if __name__ == "__main__":

    init_storage()

    main()
