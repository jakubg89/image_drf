from django.contrib.auth.models import AbstractUser
from django.db import models


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
