"""
    run worker - python -m celery -A BenzinCheck worker -l INFO
    run celery beat - python -m celery -A BenzinCheck beat -l INFO
    run celery and beat -  celery -A BenzinCheck worker --beat --scheduler django --loglevel=info
"""
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BenzinCheck.settings")
app = Celery("django_celery")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Add beat for the task
app.conf.beat_schedule = {
    'add-every-day-at-00-10': {
        'task': 'fuel.tasks.update_data_auto',
        'schedule': crontab(hour='11',
                            minute=5,
                            ),
        'args': ()
    },
}
app.autodiscover_tasks()

