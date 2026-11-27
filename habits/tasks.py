from datetime import timezone

import requests
from celery import shared_task

from config import settings
from habits.models import Habit


@shared_task
def send_telegram_message(chat_id, text):
    token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    response = requests.post(url, data=payload)
    return response.json()


@shared_task
def check_habits_for_reminders():
    now = timezone.localtime(timezone.now())
    habits_to_remind = Habit.objects.filter(
        time__hour=now.hour,
        time__minute=now.minute
    )
    for habit in habits_to_remind:
        if hasattr(habit.user, "profile") and habit.user.profile.telegram_chat_id:
            chat_id = habit.user.profile.telegram_chat_id
            text = f"Напоминание! Пора выполнить привычку: {habit.action} в {habit.place}"
            send_telegram_message(chat_id, text)