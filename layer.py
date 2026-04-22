import os
import tarfile
import hashlib

LAYERS_DIR = "/home/nithin/.docksmith/layers"


def create_layer(root, created_by=""):

    tar_path = os.path.join(LAYERS_DIR, "temp_layer.tar")

    with tarfile.open(tar_path, "w") as tar:
        tar.add(root, arcname="")

    with open(tar_path, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()

    final_name = f"sha256_{digest}.tar"
    final_path = os.path.join(LAYERS_DIR, final_name)

    os.rename(tar_path, final_path)

    size = os.path.getsize(final_path)

    return {
        "digest": f"sha256:{digest}",
        "size": size,
        "createdBy": created_by,
        "file": final_name
    }
