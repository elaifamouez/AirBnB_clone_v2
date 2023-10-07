#!/usr/bin/python3
""" This file deploy web static files in both servers """
from fabric.api import *
from datetime import datetime
from os.path import exists
env.hosts = ["34.74.224.241", "104.196.38.181"]


def do_pack():
    """Script that generates a .tgz archive from the contents of the web_static
    folder of your AirBnB Clone repo, using the function do_pack."""
    local("sudo mkdir -p versions")
    times = datetime.now().strftime("%Y%m%d%H%M%S")
    files = ("versions/web_static_{}.tgz").format(times)
    local("sudo tar -cvzf {} web_static".format(files))
    return files


def do_deploy(archive_path):
    """Script (based on the file 1-pack_web_static.py) that distributes an archive
    to your web servers, using the function do_deploy """
    if exists(archive_path) is False:
        return False
    else:
        pass
    try:
        put(archive_path, "/tmp/")
        files = archive_path.split("/")[1].split(".")[0]
        path = "/data/web_static/releases/{}".format(files)
        run("mkdir {}".format(path))
        run("tar -zxvf /tmp/{}.tgz -C {}/".format(files, path))
        run("sudo rm /tmp/{}".format(archive_path.split("/")[1]))
        run("sudo rm /data/web_static/current")
        run("sudo ln -sf /data/web_static/releases/{}\
        /data/web_static/current".format(files))
        run("sudo mv /data/web_static/releases/{}/web_static/*\
        /data/web_static/releases/{}".format(files, files))
        run("rm -rf /data/web_static/releases/{}/web_static/".format(files))
        return True
    except:
        return False
