#!/usr/bin/python3
"""
Script based on `1-pack_web_static.py` that distributes
to web servers
"""

import os
from datetime import datetime
from fabric.api import env, local, put, sudo, run, runs_once
import re


env.hosts = ['100.26.226.113', '35.175.130.55']


@runs_once
def do_pack():
    """Generates an archive of the static files"""
    if not os.path.isdir("versions"):
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
        local("tar -cvzf {} ./web_static".format(output))
        archive_size = os.stat(output).st_size
        print("web_static packed: {} -> {} Bytes".format(output, archive_size))
    except Exeption:
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
    success = False
    try:
        put(archive_path, "/tmp/{}".format(file_name))
        run("mkdir -p {}".format(folder_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))
        run("rm -rf /tmp/{}".format(file_name))
        run("mv {}web_static/* {}".format(folder_path, folder_path))
        run("rm -rf {}web_static".format(folder_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_path))
        print("New version deployed!")
        success = True
    except Exception:
        success = False
    return success


def deploy():
    """
    Archives and deploys the static files to the host servers.
    """
    archive_path = do_pack()
    return do_deploy(archive_path) if archive_path else False


def do_clean(number=0):
    """
    Deletes out-of-date archives of the static file
    Args:
        number of archives to be kept.
    """
    archives = os.listdir('versions/')
    archives.sort(reverse=True)
    start = int(number)
    if not start:
        start += 1
    if start < len(archives):
        archives = archives[start:]
    else:
        archives = []
    for archive in archives:
        os.unlink('versions/{}'.format(archive))
    cmd_parts = [
        "rm -rf $(",
        "find /data/web_static/releases/ -maxdepth 1 -type d -iregex",
        " '/data/web_static/releases/web_static_.*'",
        " | sort -r | tr '\\n' ' ' | cut -d ' ' -f{}-)".format(start + 1)
    ]
    run(''.join(cmd_parts))
