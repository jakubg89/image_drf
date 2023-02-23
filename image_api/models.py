from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
)

from functools import partial
from PIL import Image
from io import BytesIO
import sys
import uuid
from datetime import timedelta
from django.utils import timezone


class User(AbstractUser):
    tier = models.ForeignKey(
        "Tier",
        related_name="tier",
        on_delete=models.PROTECT,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "user"


class Tier(models.Model):

    tier_name = models.CharField(
        db_column="tier_name", max_length=128, verbose_name="Tier name"
    )
    max_height_small = models.IntegerField(
        blank=False, null=True, verbose_name="Max height for small thumbnail"
    )
    max_height_medium = models.IntegerField(
        blank=False, null=True, verbose_name="Max height for medium thumbnail"
    )
    show_small_thumbnail = models.BooleanField(
        blank=False,
        default=False,
        verbose_name="Allow to display small thumbnail",
    )
    show_medium_thumbnail = models.BooleanField(
        blank=False,
        default=False,
        verbose_name="Allow to display medium thumbnail",
    )
    show_original_image = models.BooleanField(
        blank=False,
        default=False,
        verbose_name="Allow to display original image",
    )
    show_temp_link = models.BooleanField(
        blank=False,
        default=False,
        verbose_name="Allow to generate temporary link",
    )

    class Meta:
        managed = True
        db_table = "tier"

    def __str__(self):
        return self.tier_name


def get_upload_path(instance, file_name, image_type):
    return f"uploads/{instance.user}/{image_type}/{file_name}"


class Picture(models.Model):
    img_type_validator = FileExtensionValidator(
        allowed_extensions=["jpg", "png", "jpeg"]
    )

    user = models.ForeignKey(
        "User", related_name="user", on_delete=models.CASCADE
    )

    original_image = models.ImageField(
        upload_to=partial(get_upload_path, image_type="original_images"),
        validators=[img_type_validator],
    )

    small_thumbnail = models.ImageField(
        blank=True,
        null=True,
        upload_to=partial(get_upload_path, image_type="small_thumbnail"),
        validators=[img_type_validator],
    )

    medium_thumbnail = models.ImageField(
        blank=True,
        null=True,
        upload_to=partial(get_upload_path, image_type="medium_thumbnail"),
        validators=[img_type_validator],
    )

    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = "picture"

    def save(self, *args, **kwargs):
        user = self.user

        image = Image.open(self.original_image)
        file_format = image.format
        file_mime = Image.MIME[image.format]
        image = image.convert("RGB")
        image.load()

        if user.tier.show_small_thumbnail and user.tier.max_height_small:
            if image.height > user.tier.max_height_small:
                new_height = user.tier.max_height_small
                self.small_thumbnail = self._create_thumbnail(
                    new_height=new_height,
                    image=image,
                    file_format=file_format,
                    file_mime=file_mime,
                )
            else:
                self.small_thumbnail = self._save_copy(
                    file_mime=file_mime, file_format=file_format, image=image
                )

        if user.tier.show_medium_thumbnail and user.tier.max_height_medium:
            if image.height > user.tier.max_height_medium:
                new_height = user.tier.max_height_medium
                self.medium_thumbnail = self._create_thumbnail(
                    new_height=new_height,
                    image=image,
                    file_format=file_format,
                    file_mime=file_mime,
                )
            else:
                self.small_thumbnail = self._save_copy(
                    file_mime=file_mime, file_format=file_format, image=image
                )
        super().save(*args, **kwargs)

    def _create_thumbnail(self, new_height, image, file_format, file_mime):
        file_name = "".join([str(uuid.uuid4()), ".", file_format])
        output = BytesIO()
        new_width = int(new_height / (image.height / image.width))
        image_resized_2 = image.resize((new_width, new_height), Image.LANCZOS)
        image_resized_2.save(output, format=file_format)
        output.seek(0)
        return InMemoryUploadedFile(
            output,
            "ImageField",
            file_name,
            file_mime,
            sys.getsizeof(output),
            None,
        )

    def _save_copy(self, file_mime, file_format, image):
        file_name = "".join([str(uuid.uuid4()), ".", file_format])
        output = BytesIO()
        image.save(output, format=file_format)
        output.seek(0)
        return InMemoryUploadedFile(
            output,
            "ImageField",
            file_name,
            file_mime,
            sys.getsizeof(output),
            None,
        )


class TempUrl(models.Model):
    picture = models.ForeignKey(
        "Picture", related_name="picture", on_delete=models.CASCADE
    )
    created = models.DateTimeField()
    url_duration = models.IntegerField(
        blank=True,
        null=True,
        validators=[
            MaxValueValidator(30000),
            MinValueValidator(300)
        ],
    )
    expiration_date = models.DateTimeField()
    alias = models.CharField(max_length=16)

    def save(self, *args, **kwargs):
        time_now = timezone.now()

        seconds = int(self.url_duration or 0)
        expiration_date = time_now + timedelta(seconds=seconds)

        self.created = time_now
        self.expiration_date = expiration_date
        self.alias = str(uuid.uuid4())[0:17]

        super().save(*args, **kwargs)
