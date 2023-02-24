# Generated by Django 4.1.7 on 2023-02-24 08:23

from django.db import migrations


def add_tier(apps, schema_editor):
    tier_model = apps.get_model('image_api', 'Tier')
    tier_model.objects.create(
        tier_name='Basic',
        max_height_small=200,
        max_height_medium=400,
        show_small_thumbnail=True,
        show_medium_thumbnail=False,
        show_original_image=False,
        show_temp_link=False,
    )
    tier_model.objects.create(
        tier_name='Premium',
        max_height_small=200,
        max_height_medium=400,
        show_small_thumbnail=True,
        show_medium_thumbnail=True,
        show_original_image=True,
        show_temp_link=False,
    )
    tier_model.objects.create(
        tier_name='Enterprise',
        max_height_small=200,
        max_height_medium=400,
        show_small_thumbnail=True,
        show_medium_thumbnail=True,
        show_original_image=True,
        show_temp_link=True,
    )


class Migration(migrations.Migration):

    dependencies = [
        ("image_api", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_tier),
    ]
