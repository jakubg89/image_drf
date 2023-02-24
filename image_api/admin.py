from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Picture, Tier, TempUrl



class PictureInline(admin.TabularInline):
    model = Picture
    readonly_fields = ("original_image", "small_thumbnail", "medium_thumbnail")
    extra = 0
    classes = ["collapse"]


class CustomUserAdmin(UserAdmin):
    fieldsets = ((None, {"fields": ("tier",)}),)

    inlines = [
        PictureInline,
    ]

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "tier"),
            },
        ),
    )
    list_display = ("username", "tier", "is_staff", "is_active")


admin.site.register(User, CustomUserAdmin)


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    search_fields = ("user",)
    fields = ("user", "original_image")
    list_filter = ("user",)
    list_display = (
        "id",
        "user",
        "small_thumbnail",
        "medium_thumbnail",
        "original_image",
    )


@admin.register(Tier)
class TierAdmin(admin.ModelAdmin):

    list_display = (
        "tier_name",
        "max_height_small",
        "max_height_medium",
        "show_small_thumbnail",
        "show_medium_thumbnail",
        "show_original_image",
        "show_temp_link",
    )

    list_filter = (
        "show_small_thumbnail",
        "show_medium_thumbnail",
        "show_original_image",
        "show_temp_link",
    )

    search_fields = ("tier_name",)


@admin.register(TempUrl)
class TempUrlAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created",
        "expiration_date",
        "url_duration",
    )
