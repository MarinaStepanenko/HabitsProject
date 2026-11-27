from rest_framework import generics, permissions
from rest_framework.decorators import permission_classes

from users.serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


