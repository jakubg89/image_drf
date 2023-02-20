from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from image_api.models import User, Tier
import tempfile
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class UserUploadImageTestCase(APITestCase):
    def test_unauthorized_access_to_upload_image(self):
        self.client.logout()
        response = self.client.get(reverse("upload"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_user_get_method(self):
        url = reverse("upload")
        user = User.objects.create_user("user-test", "pass-test")
        self.client.force_login(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wrong_file_upload(self):
        url = reverse("upload")
        tier = Tier.objects.create(tier_name="Basic", show_small_thumbnail=True)
        user = User.objects.create_user(
            username="user-test",
            password="pass-test",
            tier=tier)
        self.client.force_login(user)

        with tempfile.TemporaryFile(suffix=".gif") as temp:
            image = Image.new("RGB", (100, 100), (255, 255, 255))
            image.save(temp, format="gif")
            temp.seek(0)
            response = self.client.post(url, {'original_image': temp}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_data_post(self):
        url = reverse("upload")
        user = User.objects.create_user("user-test", "pass-test")
        self.client.force_login(user)

        wrong_data = {"original_image": "tefdgfg"}
        response = self.client.post(url, wrong_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserPictureListTestCase(APITestCase):
    def test_unauthorized_access_to_picture_list(self):
        self.client.logout()
        response = self.client.get(reverse("image-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_user(self):
        user = User.objects.create_user("user-test", "pass-test")
        self.client.force_login(user)
        response = self.client.get(reverse("image-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserUrlListTestCase(APITestCase):
    def test_access_to_url_list(self):
        self.client.logout()
        response = self.client.get(reverse("user-root"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
