from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from django.conf import settings


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="habits",
                             verbose_name="Пользователь"
                             )
    place = models.CharField(max_length=250, verbose_name="место"),
    time = models.DateTimeField(verbose_name="Время")
    action = models.CharField(max_length=350, verbose_name="Действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Признак приятной привычки")
    related_habit = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Связанная привычка")
    periodicity = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(7)],
                                              verbose_name="Периодичность в днях"
                                              )
    reward = models.CharField(max_length=255, null=True, blank=True, verbose_name="Вознаграждение")
    duration = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(120)],
        verbose_name="Время на выполнение в секундах"
    )
    is_public = models.BooleanField(default=False, verbose_name="Признак публичности привычки")

    def clean(self):
        if self.related_habit and self.reward:
            raise ValidationError("Нельзя одновременно указать связанную привычку и вознаграждение")

        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной")

        if self.is_pleasant:
            if self.related_habit or self.reward:
                raise ValidationError("У приятной привычки не может быть вознаграждения иди связанной привычки")

    def __str__(self):
        return f"{self.action} в {self.time} в {self.place}"
