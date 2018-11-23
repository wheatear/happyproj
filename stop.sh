
# stop nginx
nginx -s stop
# stop uwsgi
workon py37
uwsgi --stop uwsgi.pid
