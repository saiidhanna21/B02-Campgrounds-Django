# Generated by Django 5.0.3 on 2024-03-23 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campgrounds', '0018_remove_campgrounds_rating_campgrounds_average_rating_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campgrounds',
            name='average_rating',
        ),
        migrations.AddField(
            model_name='campgrounds',
            name='rating',
            field=models.CharField(choices=[('NR', 'Not Rated'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], default='NR', max_length=10),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='rating',
            field=models.CharField(choices=[('NR', 'Not Rated'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], default='NR', max_length=10),
        ),
    ]
