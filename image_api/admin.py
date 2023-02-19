from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Picture


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
