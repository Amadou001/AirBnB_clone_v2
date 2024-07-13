#!/usr/bin/python3
""" 2-do_deploy_web_static module"""

import os
from datetime import datetime
from fabric.api import env, local, put, run, runs_once


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
        return None


def do_deploy(archive_path):
    """do deploy function: Function that take the content

    Args:
        archive_path (string): Path of the archive file

    Returns:
        False if an exception occured
    """
    if not os.path.exists(archive_path):
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
