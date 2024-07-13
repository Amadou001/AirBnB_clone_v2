#!/usr/bin/python3
"""
Fabric script for cleaning up old deployments and archives
"""

from fabric.api import env, local, run

# Environment configuration
env.hosts = ['54.144.139.236', '54.242.186.62']
env.user = 'ubuntu'  # Update with your username
# Update with your SSH key path
env.key_filename = '/path/to/your/ssh/private_key'


def do_clean(number=0):
    """
    Cleans up old deployments and archives
    """
    try:
        number = int(number)
        if number < 1:
            number = 1

        # Clean up local versions directory
        versions_dir = 'versions'
        local_clean_command = 'ls -t {}/ | tail -n +{}\
              | xargs -I {{}} rm -f {}/{{}}'.format(
            versions_dir, number + 1, versions_dir
        )
        local(local_clean_command)

        # Clean up remote releases directory
        releases_dir = '/data/web_static/releases'
        remote_clean_command = 'ls -t {} | tail -n +{}\
              | xargs -I {{}} rm -rf {}/{{}}'.format(
            releases_dir, number + 1, releases_dir
        )
        run(remote_clean_command)

    except ValueError:
        pass
