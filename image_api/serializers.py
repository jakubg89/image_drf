from django.conf import settings

from image_api.models import User, Picture, Tier, TempUrl
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    tier_name = serializers.CharField(source="tier.tier_name", read_only=True)
    user_img = serializers.SerializerMethodField("get_image_url")

    def get_image_url(self, user_obj):
        user_name = getattr(user_obj, "id")
        return Picture.objects.filter(user=user_name).values(
            "id", "original_image", "small_thumbnail", "medium_thumbnail"
        )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "tier",
            "tier_name",
            "user_img",
        ]


class PictureUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ["original_image"]
        extra_kwargs = {"original_image": {"required": True}}

    def get_picture_pk(self, obj):
        return obj.pk

    def get_small_thumbnail(self, obj):
        return obj.small_thumbnail.url

    def get_original_image(self, obj):
        return obj.original_image.url

    def get_medium_thumbnail(self, obj):
        return obj.medium_thumbnail.url

    def to_representation(self, instance):
        HOST_NAME = settings.HOST_NAME
        data = super(PictureUserSerializer, self).to_representation(instance)

        user = instance.user

        if user.tier.show_small_thumbnail:
            small_thumbnail_url = "".join(
                [HOST_NAME, self.get_small_thumbnail(instance)]
            )
            data["small_thumbnail"] = small_thumbnail_url

        if user.tier.show_medium_thumbnail:
            medium_thumbnail = "".join(
                [HOST_NAME, self.get_medium_thumbnail(instance)]
            )
            data["medium_thumbnail"] = medium_thumbnail

        if user.tier.show_original_image:
            original_image = "".join(
                [HOST_NAME, self.get_original_image(instance)]
            )
            data["original_image"] = original_image
        else:
            data.pop("original_image")
        if user.tier.show_temp_link:
            data.update(
                {
                    "get_download_url":
                        f"{HOST_NAME}/get-url/{self.get_picture_pk(instance)}"
                }
            )
        return data


# Tier serializer for detail view of each tier.
class TierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tier
        fields = [
            "id",
            "tier_name",
            "max_height_small",
            "max_height_medium",
            "show_small_thumbnail",
            "show_medium_thumbnail",
            "show_original_image",
            "show_temp_link",
        ]


class PictureStaffSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Picture
        fields = [
            "id",
            "small_thumbnail",
            "medium_thumbnail",
            "original_image",
        ]


class TempUrlSerializer(serializers.ModelSerializer):
    url_duration = serializers.IntegerField(
        min_value=300,
        max_value=30000,
        error_messages={
            "min_value": "Ensure this value is greater than or equal to 300 "
            "and less than or equal to 30000.",
            "max_value": "Ensure this value is greater than or equal to 300 "
            "and less than or equal to 30000.",
        },
    )
    picture = serializers.CharField(
        source="picture.original_image",
        read_only=True
    )
    expiration_date = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True
    )
    alias = serializers.CharField(read_only=True)

    class Meta:
        model = TempUrl
        fields = ["picture", "url_duration", "expiration_date", "alias"]
        extra_kwargs = {"url_duration": {"required": True}}

    def to_representation(self, instance):
        HOST_NAME = settings.HOST_NAME
        data = super(TempUrlSerializer, self).to_representation(instance)

        data["picture"] = "".join([HOST_NAME, "/", data["picture"]])

        data["alias"] = "".join([HOST_NAME, "/download/", data["alias"]])
        return data
