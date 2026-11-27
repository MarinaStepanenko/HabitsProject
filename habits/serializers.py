from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):


    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user",)

    def validate(self, attr):
        related_habit = attr.get("related_habit")
        reward = attr.get("reward")
        is_pleasant = attr.get("is_pleasant")

        if related_habit and reward:
            raise serializers.ValidationError("Нельзя одновременно указать связанную привычку и вознаграждение")

        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError("Связанная привычка должна быть приятной")

        if is_pleasant:
            if related_habit or reward:
                raise serializers.ValidationError("У приятной привычки не может быть вознаграждения иди связанной привычки")

        return attr
