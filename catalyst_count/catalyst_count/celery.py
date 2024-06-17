from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catalyst_count.settings')

app = Celery('catalyst_count')

app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.update(
    worker_max_tasks_per_child=1000,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    worker_concurrency=10,
    worker_max_memory_per_child=500000,  
)


app.autodiscover_tasks()