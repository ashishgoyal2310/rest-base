from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
import socket

# Get hostname
# _host = socket.gethostname()

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.task(bind=True)
def debug_redis_connection(self):
    import redis, time
    redis_conn = redis.Redis(host=settings.REDIS_HOST, port=6379)

    retries = 3
    count = "Zero"
    while True:
        try:
            count = redis_conn.incr('hits')
            break
        except redis.exceptions.ConnectionError as exc:
            print('Retry left: {} Redis connection: {}'.format(retries, redis_conn))
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)
        except Exception as exc:
            raise exc
    print('Request: {0!r}, Total hits'.format(self.request, count))