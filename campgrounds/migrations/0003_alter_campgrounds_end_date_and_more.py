# Generated by Django 5.0.3 on 2024-03-20 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campgrounds', '0002_campgrounds_user_reviews_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campgrounds',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='campgrounds',
            name='start_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
