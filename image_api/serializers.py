from image_api.models import User, Picture, Tier
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    tier_name = serializers.CharField(source="tier.tier_name", read_only=True)
    user_img = serializers.SerializerMethodField("get_image_url")

    def get_image_url(self, user_obj):
        user_name = getattr(user_obj, "id")
        return Picture.objects.filter(username=user_name).values(
            "id", "original_image", "small_thumbnail", "medium_thumbnail"
        )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "tier",
            "tier_name",
            "user_img",
        ]


class PictureSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(
        source="user.username", read_only=True
    )
    small_thumbnail = serializers.CharField(read_only=True)
    medium_thumbnail = serializers.CharField(read_only=True)

    class Meta:
        model = Picture
        fields = [
            "id",
            "username",
            "original_image",
            "small_thumbnail",
            "medium_thumbnail",
        ]

    def get_username(self, obj):
        return obj.username.username


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