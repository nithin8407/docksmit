import os
import shutil
import subprocess

def execute_copy(src, dest, context, root):

    src_path = os.path.join(context, src)
    dest_path = os.path.join(root, dest.lstrip("/"))

    os.makedirs(dest_path, exist_ok=True)

    for item in os.listdir(src_path):

        s = os.path.join(src_path, item)
        d = os.path.join(dest_path, item)

        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)


def execute_run(cmd, root):

    os.makedirs(os.path.join(root, "usr/bin"), exist_ok=True)

    if not os.path.exists(os.path.join(root, "usr/bin/python3")):
        shutil.copy("/usr/bin/python3", os.path.join(root, "usr/bin/python3"))

    subprocess.run(
        cmd,
        shell=True,
        cwd=root,
        env=os.environ.copy(),
        check=True
    )
