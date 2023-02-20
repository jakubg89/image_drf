from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from image_api.models import User


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
