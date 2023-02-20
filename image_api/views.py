from django.conf import settings
from django.urls import get_resolver

from rest_framework.authentication import SessionAuthentication
from rest_framework import permissions
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from image_api.models import User, Picture, Tier
from image_api.serializers import (
    UserSerializer,
    PictureSerializer,
    TierSerializer,
    UserUploadImageSerializer,
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


class UserRoot(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        url_patterns = get_resolver().url_patterns
        allowed_urls = [
            "upload/",
            "image-list/",
        ]
        if request.user.is_authenticated:
            if self.request.user.tier.show_temp_link:
                allowed_urls.append("download/")
        urls = {}
        for pattern in url_patterns:
            if str(pattern.pattern) in allowed_urls:
                name = pattern.resolve(str(pattern.pattern))
                url = "".join(
                    [settings.HOST_NAME, "/", str(pattern.pattern)]
                )
                urls.update({name.url_name: url})
        return Response(urls)


class UserUploadImage(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = UserUploadImageSerializer
    authentication_classes = [SessionAuthentication]

    def post(self, request, format=None):
        serializer = UserUploadImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(username=self.request.user)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response()

    def perform_create(self, serializer):
        serializer.save(username=self.request.user)


class UserPictureList(APIView):
    queryset = Picture.objects.all()
    serializer_class = UserUploadImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get(self, request):
        pictures = self.queryset.filter(username=request.user)
        serializer = self.serializer_class(pictures, many=True)
        return Response(serializer.data)
