from image_api.models import User, Picture, Tier

from rest_framework.authentication import SessionAuthentication
from rest_framework import permissions

from rest_framework import viewsets
from image_api.serializers import (
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [SessionAuthentication]
