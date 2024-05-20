import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.core.settings')

app = Celery('celery')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(
    [
        "src.apps.trading_platform.tasks",
    ],
)

app.conf.beat_schedule = {
    "start_test_task": {
        "task": "src.apps.trading_platform.tasks.test_task",
        "schedule": 1,
    }
}
