# Generated by Django 5.0.3 on 2024-03-20 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campgrounds', '0004_alter_campgrounds_start_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campgrounds',
            name='image',
        ),
        migrations.AlterField(
            model_name='campgrounds',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='campgrounds',
            name='start_date',
            field=models.DateField(),
        ),
    ]
