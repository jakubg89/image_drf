from image_api.models import User, Picture, Tier

from rest_framework.authentication import SessionAuthentication
from rest_framework import permissions

from rest_framework import viewsets
from image_api.serializers import (
    UserSerializer,
    PictureSerializer,
    TierSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [SessionAuthentication]


class PicturesViewSet(viewsets.ModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [SessionAuthentication]

    def perform_create(self, serializer):
        serializer.save(username=self.request.user)


class TierViewSet(viewsets.ModelViewSet):
    queryset = Tier.objects.all()
    serializer_class = TierSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [SessionAuthentication]
