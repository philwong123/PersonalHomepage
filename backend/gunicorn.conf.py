import multiprocessing
import os

from gevent import monkey

monkey.patch_all()

chdir = os.path.dirname(os.path.abspath(__file__))

bind = '0.0.0.0:5000'
backlog = 2048
timeout = 60
worker_class = 'gevent'

workers = multiprocessing.cpu_count() * 2 + 1
threads = multiprocessing.cpu_count() * 2
daemon = False

loglevel = 'info'
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'

accesslog = 'logs/gunicorn_access.log'
errorlog = 'logs/gunicorn_error.log'

pidfile = 'logs/gunicorn.pid'
