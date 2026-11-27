from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import permission_classes
from rest_framework.pagination import PageNumberPagination

from habits.models import Habit
from habits.permissions import IsOwnerOrReadOnly
from habits.serializers import HabitSerializer


class HabitPagination(PageNumberPagination):
    page_size = 5


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [permissions.AllowAny] #[permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        if self.action == "list":
            return Habit.objects.filter(user=self.request.user) | Habit.objects.filter(is_public=True)

        return Habit.objects.filter(user=self.request.user)


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
