# Generated by Django 5.1.1 on 2024-11-11 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_time_pause_end_pause'),
    ]

    operations = [
        migrations.AddField(
            model_name='sport',
            name='sets',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
