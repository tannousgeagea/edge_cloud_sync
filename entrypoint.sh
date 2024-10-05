#!/bin/bash
set -e

/bin/bash -c "python3 /home/$user/src/edge_cloud_sync/manage.py makemigrations"
/bin/bash -c "python3 /home/$user/src/edge_cloud_sync/manage.py migrate"
/bin/bash -c "python3 /home/$user/src/edge_cloud_sync/manage.py create_superuser"

sudo -E supervisord -n -c /etc/supervisord.conf