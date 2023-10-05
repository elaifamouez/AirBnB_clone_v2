#!/usr/bin/python3
"""
Fabric script for deploying an archive to web servers
"""

from fabric.api import put, run, env
from os.path import exists

env.hosts = ['100.26.156.69', '54.174.114.135']


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    if not exists(archive_path):
        return False

    try:
        file_name = archive_path.split("/")[-1]
        name = file_name.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        run("mkdir -p {}{}/".format(path, name))
        run("tar -xzf /tmp/{} -C {}{}/".format(file_name, path, name))
        run("rm /tmp/{}".format(file_name))
        run("rm -rf /data/web_static/current")
        run("ln -s {}{}/ /data/web_static/current".format(path, name))
        return True
    except BaseException:
        return False
