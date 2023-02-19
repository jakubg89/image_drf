from django.contrib import admin
from django.urls import include, path

from image_api import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"staff/users", views.UserViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("staff/", include(router.urls)),
    path(
        "api-auth/", include("rest_framework.urls", namespace="rest_framework")
    ),
]
