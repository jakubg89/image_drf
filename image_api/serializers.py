from django.conf import settings

from image_api.models import User, Picture, Tier
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


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = []

    def get_small_thumbnail(self, obj):
        return obj.small_thumbnail.url

    def get_original_image(self, obj):
        return obj.original_image.url

    def get_medium_thumbnail(self, obj):
        return obj.medium_thumbnail.url

    def to_representation(self, instance):
        HOST_NAME = settings.HOST_NAME
        data = super(
            PictureSerializer, self
        ).to_representation(instance)

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
            data.update({"download_org_img": "jakies url"})
            # todo pass picture id
           #  f'{HOST_NAME}/downloads/{instance.user}'
        return data


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


class UserUploadImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Picture
        fields = ["original_image"]
        extra_kwargs = {"original_image": {"required": True}}

    def get_small_thumbnail(self, obj):
        return obj.small_thumbnail.url

    def get_original_image(self, obj):
        return obj.original_image.url

    def get_medium_thumbnail(self, obj):
        return obj.medium_thumbnail.url

    def to_representation(self, instance):
        HOST_NAME = settings.HOST_NAME

        data = super(
            UserUploadImageSerializer, self
        ).to_representation(instance)

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

        return data

