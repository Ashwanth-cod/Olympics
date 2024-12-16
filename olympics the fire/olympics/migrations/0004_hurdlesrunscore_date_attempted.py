# Generated by Django 4.2.16 on 2024-11-03 04:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('olympics', '0003_remove_hurdlesrunscore_attempts_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hurdlesrunscore',
            name='date_attempted',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
