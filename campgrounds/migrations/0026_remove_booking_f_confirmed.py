# Generated by Django 5.0.3 on 2024-03-23 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campgrounds', '0025_alter_campgrounds_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='f_confirmed',
        ),
    ]
