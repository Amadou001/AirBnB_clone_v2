#!/usr/bin/python3
""" 3-do_deploy_web_static module"""

from fabric.api import env, run, put, local
import os
from datetime import datetime

env.hosts = ['54.144.139.236', '54.242.186.62']


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    Returns the archive path if correctly generated, otherwise None.
    """
    try:
        if not os.path.exists("versions"):
            os.makedirs("versions")

        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        archive_name = "web_static_{}.tgz".format(timestamp)

        local("tar -cvzf versions/{} web_static".format(archive_name))

        return "versions/{}".format(archive_name)

    except Exception as e:
        print("Packaging failed:", e)
        return None


def do_deploy(archive_path):
    """Deploy function: Uploads and deploys an archive to web servers

    Args:
        archive_path (string): Path of the archive file

    Returns:
        False if deployment fails
    """
    if not os.path.exists(archive_path):
        print(f"Archive {archive_path} not found.")
        return False

    try:
        my_archive = os.path.basename(archive_path)
        put(archive_path, '/tmp/{}'.format(my_archive))

        release_dir = '/data/web_static/releases/{}'.format(
            my_archive.replace('.tgz', '')
        )

        run('mkdir -p {}'.format(release_dir))

        run('tar -xzf /tmp/{} -C {}'.format(my_archive, release_dir))

        run('rm /tmp/{}'.format(my_archive))

        run('mv {}/web_static/* {}'.format(release_dir, release_dir))

        run('rm -rf {}/web_static'.format(release_dir))

        current_link = '/data/web_static/current'
        run('rm -rf {}'.format(current_link))

        run('ln -s {} {}'.format(release_dir, current_link))

        print("New version deployed!")
        return True

    except Exception as e:
        print("Deployment failed:", e)
        return False


def deploy():
    """Full deployment"""
    archive_path = do_pack()
    if archive_path:
        return do_deploy(archive_path)
    else:
        return False
