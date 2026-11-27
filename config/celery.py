import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('HabitsProject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# --- Расписание задач (вместо django-celery-beat) ---
app.conf.beat_schedule = {
    'check-habits-every-minute': {
        'task': 'habits.tasks.check_habits_for_reminders',
        'schedule': 60.0,  # Каждые 60 секунд
    },
}