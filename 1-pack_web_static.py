#!/usr/bin/env python3
"""
Fabric script that generates a .tgz archive from the contents
of the web_static folder of your AirBnB Clone repo
"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    Returns the archive path if successful, otherwise, returns None
    """
    try:
        # Create the 'versions' folder if it doesn't exist
        local("mkdir -p versions")

        # Generate the archive path
        archive_path = "versions/web_static_{}.tgz".format(
            datetime.now().strftime("%Y%m%d%H%M%S")
        )

        # Create the .tgz archive
        local("tar -cvzf {} web_static".format(archive_path))

        # Return the archive path if successful
        return archive_path
    except Exception:
        # Return None if an error occurs
        return None
