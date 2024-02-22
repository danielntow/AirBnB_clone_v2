#!/usr/bin/python3
"""
Script based on `1-pack_web_static.py` that distributes to web servers
"""

import os
from datetime import datetime
from fabric.api import env, local, put, run, runs_once

env.hosts = ['100.26.226.113', '34.234.193.247']


@runs_once
def do_pack():
    """Generates an archive of the static files"""
    if not os.path.exists("versions"):
        os.mkdir("versions")
    c_time = datetime.now()
    output = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        c_time.year,
        c_time.month,
        c_time.day,
        c_time.hour,
        c_time.minute,
        c_time.second
    )
    try:
        print("Packing web_static to {}".format(output))
        local("tar -czvf {} ./web_static".format(output))
        archive_size = os.stat(output).st_size
        print("web_static packed: {} -> {} Bytes".format(output, archive_size))
    except Exception as e:
        print("Error during packing: {}".format(e))
        output = None
    return output


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
    folder_path = "/data/web_static/releases/{}/".format(folder_name)
    try:
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(folder_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))
        run("rm /tmp/{}".format(file_name))
        run("mv {}web_static/* {}".format(folder_path, folder_path))
        run("rm -rf {}web_static".format(folder_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_path))
        print("New version deployed!")
        return True
    except Exception as e:
        print("Error during deployment: {}".format(e))
        return False
