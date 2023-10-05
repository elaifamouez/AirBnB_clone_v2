#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""
from fabric.api import run, put, env, sudo
import os

# Define hosts and user
env.hosts = ['100.26.156.69', '54.174.114.135']
env.user = "ubuntu"


def do_deploy(archive_path):
    """
    Distributes an archive to web servers

    Args:
        archive_path: Path to where the archive is stored locally

    Returns:
        True: If all operations have been done correctly
        False: If any operation fails, like if archive_path doesn't exist
    """
    # Make sure archive path exists
    if not os.path.isfile(archive_path):
        return False

    try:
        # Get archive file (without leading path)
        archive_file = os.path.basename(archive_path)

        # Get folder name
        folder = archive_file.split('.')[0]

        # Extraction path (where archive will be extracted)
        extract_path = f"/data/web_static/releases/{folder}"

        # Upload the archive to /tmp/ folder of remote server
        upload = put(archive_path, '/tmp/')

        # Check if upload failed
        if upload.failed:
            return False

        # Create folder in remote server
        create = run(f"mkdir -p {extract_path}")

        # Check folder creation
        if create.failed:
            return False

        # Uncompress the archive to the folder /data/web_static/releases
        extract = run(f"tar -xzf /tmp/{archive_file} -C {extract_path}/")

        # Check if extraction failed
        if extract.failed:
            return False

        # Delete the archive from remote server
        del_archive = run(f"sudo rm /tmp/{archive_file}")

        if del_archive.failed:
            return False

        # Move extracted content to new folder
        move_extracted = run(f"mv {extract_path}/web_static/* {extract_path}/")

        if move_extracted.failed:
            return False

        # Remove extracted folder (web_static) in remote server
        del_folder = run(f"sudo rm -rf {extract_path}/web_static")

        if del_folder.failed:
            return False

        # Delete symbolic link (/data/web_static/current) from remote server
        del_sym = run('sudo rm -rf /data/web_static/current')

        if del_sym.failed:
            return False

        # Create new symbolic link (/data/web_static/current)
        new_sym = run(f"sudo ln -s {extract_path}/ /data/web_static/current")

        if new_sym.failed:
            return False

        print("New version deployed!")

        return True
    except Exception:
        return False
