from django.contrib import admin
from django.urls import include, path

from image_api import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"staff/users", views.UserViewSet)
router.register(r"staff/pictures", views.PicturesViewSet)
router.register(r"staff/tiers", views.TierViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("staff/", include(router.urls)),
    path(
        "api-auth/", include("rest_framework.urls", namespace="rest_framework")
    ),

    # for users urls
    path("", views.UserUrlList.as_view()),
    path("upload/", views.UserUploadImage.as_view(), name="upload"),
    path("image-list/", views.UserPictureList.as_view(), name="image_list"),
]
