from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers

from image_api import views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"pictures", views.PicturesViewSet)
router.register(r"tiers", views.TierViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("staff/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # for users urls
    path("", views.UserRoot.as_view(), name="user-root"),
    path("upload/", views.UserUploadImage.as_view(), name="upload"),
    path("image-list/", views.UserPictureList.as_view(), name="image-list"),
    path("get-url/<int:picture>", views.GenerateTempURL.as_view(), name="generate-url"),
    path("download/<str:alias>", views.ServeFile, name="download-file"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
