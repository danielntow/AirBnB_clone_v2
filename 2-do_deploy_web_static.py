#!/usr/bin/python3
"""
Script to distribute an archive to web servers
"""

from fabric.api import put, run, env
from os.path import exists
from datetime import datetime

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'
env.key_filename = 'private_key.pem'  # Replace with your private key filename


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Extract the archive to the folder /data/web_static/releases/<archive filename without extension>
        filename = archive_path.split('/')[-1]
        folder_path = "/data/web_static/releases/{}".format(
            filename.split('.')[0])
        run("mkdir -p {}".format(folder_path))
        run("tar -xzf /tmp/{} -C {}".format(filename, folder_path))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(filename))

        # Move contents to the parent folder and remove inner folder
        run("mv {}/web_static/* {}".format(folder_path, folder_path))
        run("rm -rf {}/web_static".format(folder_path))

        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link linked to the new version of your code
        run("ln -s {} /data/web_static/current".format(folder_path))

        print("New version deployed!")
        return True

    except Exception as e:
        print("Error: {}".format(e))
        return False


archive_path = "web_static_{}.tgz".format(
    datetime.now().strftime("%Y%m%d%H%M%S"))
do_deploy(archive_path)
