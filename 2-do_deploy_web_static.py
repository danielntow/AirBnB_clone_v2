#!/usr/bin/python3
"""Python module to deploy archive on web servers"""
from fabric.api import env, put, run
from os import path

env.hosts = ['100.26.226.113', '35.175.130.55']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_deploy(archive_path):
    """Deploy web files to server"""
    try:
        if not path.exists(archive_path):
            return False

        # Extracting timestamp from the archive filename
        timestamp = archive_path.split('_')[-1][:-4]

        # Uploading the archive to /tmp/ directory on the server
        put(archive_path, '/tmp/')

        # Creating the necessary directories
        run('sudo mkdir -p /data/web_static/releases/web_static_{}/'.format(timestamp))

        # Extracting the contents of the archive
        run('sudo tar -xzf /tmp/web_static_{}.tgz -C /data/web_static/releases/web_static_{}/'
            .format(timestamp, timestamp))

        # Removing the uploaded archive
        run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))

        # Moving contents to the parent folder and removing inner folder
        run('sudo mv /data/web_static/releases/web_static_{}/web_static/* '
            '/data/web_static/releases/web_static_{}/'.format(timestamp, timestamp))

        # Removing the inner web_static folder
        run('sudo rm -rf /data/web_static/releases/web_static_{}/web_static'.format(timestamp))

        # Removing the old symbolic link
        run('sudo rm -rf /data/web_static/current')

        # Creating a new symbolic link
        run('sudo ln -s /data/web_static/releases/web_static_{}/ /data/web_static/current'.format(timestamp))
    except Exception as e:
        print("Error: {}".format(e))
        return False

    return True
