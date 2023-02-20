from unittest import TestCase

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from image_api.models import User, Tier, Picture
import tempfile
from PIL import Image


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


class PictureTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.image_path = "image_api/test_images/auta.jpg"

    def test_create_picture(self):
        tier = Tier.objects.create(tier_name="Enterprise",
                                   max_height_small=200,
                                   max_height_medium=400,
                                   show_small_thumbnail=True,
                                   show_medium_thumbnail=True,
                                   show_original_image=True,
                                   show_temp_link=True)
        user = User.objects.create_user(
            username="user-test",
            password="pass-test",
            tier=tier)
        with open(self.image_path, "rb") as f:
            image_file = SimpleUploadedFile(
                "test_image.jpg", f.read(), content_type="image/jpeg"
            )
            picture = Picture.objects.create(
                username=user,
                original_image=image_file
            )

        self.assertEqual(picture.username, user)

        original_image_path = picture.original_image.path
        original_image = Image.open(original_image_path)
        self.assertEqual(original_image.width, 1600)
        self.assertEqual(original_image.height, 1066)

        small_thumbnail_path = picture.small_thumbnail.path
        small_thumbnail = Image.open(small_thumbnail_path)
        self.assertEqual(small_thumbnail.height, 200)

        medium_thumbnail_path = picture.medium_thumbnail.path
        medium_thumbnail = Image.open(medium_thumbnail_path)
        self.assertEqual(medium_thumbnail.height, 400)
