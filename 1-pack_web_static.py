#!/usr/bin/python3
"""
Script to setup Fabric and generate .tgz file
"""

from fabric.api import local
from datetime import datetime
from fabric.decorators import runs_once


@runs_once
def do_pack():
    """
    Generates .tgz archive from the content
    """
    try:
        # Create the 'versions' folder if it doesn't exist
        local("mkdir -p versions")

        # Generate the archive path
        path = "versions/web_static_{}.tgz".format(
            datetime.now().strftime("%Y%m%d%H%M%S"))

        # Create the .tgz archive
        local("tar -czvf {} ./web_static".format(path))

        return path
    except Exception as e:
        print(f"Error: {e}")
        return None
