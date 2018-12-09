#!/usr/bin/env bash

#nginx log rotate
0 0 * * *  sh /data/web/happyproj/rotate_nginxlog.sh
#uwsgi log rotate
0 0 * * * sh /data/web/happyproj/touchforuwsgilogrotate.sh
