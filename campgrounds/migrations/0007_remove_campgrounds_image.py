# Generated by Django 5.0.3 on 2024-03-20 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campgrounds', '0006_campgrounds_image_alter_campgrounds_end_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campgrounds',
            name='image',
        ),
    ]
