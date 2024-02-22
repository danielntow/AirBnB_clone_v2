#!/usr/bin/python3
"""
Fabric script to clean outdated archives
"""

from fabric.api import env, local, run, lcd

env.hosts = ['100.26.226.113', '35.175.130.55']


def do_clean(number=0):
    """
    Cleans outdated archives
    Args:
        number (int): The number of archives to keep
    """
    number = int(number)

    if number < 0:
        return

    with lcd('versions'):
        local("ls -t | tail -n +{} | xargs rm -f".format(number + 1))

    with lcd('/data/web_static/releases'):
        run("ls -t | tail -n +{} | xargs rm -rf".format(number + 1))


if __name__ == "__main__":
    pass
