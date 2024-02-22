#!/usr/bin/python3
"""
Script based on `1-pack_web_static.py` that distributes to web servers
"""

import os
from datetime import datetime
from fabric.api import env, local, put, sudo, run, runs_once

env.hosts = ['100.26.226.113', '35.175.130.55']


@runs_once
def do_pack():
    """Generates an archive of the static files"""
    output_folder = "versions"
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    current_time = datetime.now()
    output_path = f"{
        output_folder}/web_static_{current_time.strftime('%Y%m%d%H%M%S')}.tgz"

    try:
        print(f"Packing web_static to {output_path}")
        local(f"tar -czf {output_path} ./web_static")
        archive_size = os.path.getsize(output_path)
        print(f"web_static packed: {output_path} -> {archive_size} Bytes")
        return output_path
    except Exception as e:
        print(f"Error during packing: {e}")
        return None


def do_deploy(archive_path):
    """
    Deploys the static files to the host servers
    Args:
        archive_path (str): The path to the archived static files
    """
    if not os.path.exists(archive_path):
        return False

    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = f"/data/web_static/releases/{folder_name}"

    try:
        put(archive_path, "/tmp/")
        run(f"mkdir -p {folder_path}")
        run(f"tar -xzf /tmp/{file_name} -C {folder_path}")
        run(f"rm /tmp/{file_name}")
        run(f"mv {folder_path}/web_static/* {folder_path}/")
        run(f"rm -rf {folder_path}/web_static")
        run("rm -rf /data/web_static/current")
        run(f"ln -s {folder_path} /data/web_static/current")
        print("New version deployed!")
        return True
    except Exception as e:
        print(f"Error during deployment: {e}")
        return False


def deploy():
    """
    Archives and deploys the static files to the host servers.
    """
    archive_path = do_pack()
    return do_deploy(archive_path) if archive_path else False


#!/usr/bin/python3
"""
Script based on `1-pack_web_static.py` that distributes to web servers
"""


env.hosts = ['100.26.226.113', '35.175.130.55']


@runs_once
def do_pack():
    """Generates an archive of the static files"""
    output_folder = "versions"
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    current_time = datetime.now()
    output_path = f"{
        output_folder}/web_static_{current_time.strftime('%Y%m%d%H%M%S')}.tgz"

    try:
        print(f"Packing web_static to {output_path}")
        local(f"tar -czf {output_path} ./web_static")
        archive_size = os.path.getsize(output_path)
        print(f"web_static packed: {output_path} -> {archive_size} Bytes")
        return output_path
    except Exception as e:
        print(f"Error during packing: {e}")
        return None


def do_deploy(archive_path):
    """
    Deploys the static files to the host servers
    Args:
        archive_path (str): The path to the archived static files
    """
    if not os.path.exists(archive_path):
        return False

    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = f"/data/web_static/releases/{folder_name}"

    try:
        put(archive_path, "/tmp/")
        run(f"mkdir -p {folder_path}")
        run(f"tar -xzf /tmp/{file_name} -C {folder_path}")
        run(f"rm /tmp/{file_name}")
        run(f"mv {folder_path}/web_static/* {folder_path}/")
        run(f"rm -rf {folder_path}/web_static")
        run("rm -rf /data/web_static/current")
        run(f"ln -s {folder_path} /data/web_static/current")
        print("New version deployed!")
        return True
    except Exception as e:
        print(f"Error during deployment: {e}")
        return False


def deploy():
    """
    Archives and deploys the static files to the host servers.
    """
    archive_path = do_pack()
    return do_deploy(archive_path) if archive_path else False
