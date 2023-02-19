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