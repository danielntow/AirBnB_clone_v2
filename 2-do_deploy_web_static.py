#!/usr/bin/python3
"""
Fabric script that distributes an archive to my two web servers
"""

from fabric.api import env, put, run
import os

# Servers' IP addresses
env.hosts = ['100.26.226.113', '34.234.193.247']
# The user to connect as
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Distributes an archive to my two web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Uncompress the archive to the folder
        # /data/web_static/releases/<archive filename without extension>

        archive_filename = os.path.basename(archive_path)
        archive_name_no_ext = archive_filename.split('.')[0]
        releases_folder = "/data/web_static/releases/"
        release_folder = releases_folder + archive_name_no_ext + "/"
        run("mkdir -p {}".format(release_folder))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, release_folder))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(archive_filename))

        # Move contents of release_folder/web_static/ to release_folder/
        run("mv {}web_static/* {}".format(release_folder, release_folder))
        run("rm -rf {}web_static".format(release_folder))

        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s {} /data/web_static/current".format(release_folder))

        print("New version deployed!")
        return True
    except Exception as e:
        return False
