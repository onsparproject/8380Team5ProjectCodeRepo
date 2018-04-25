# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='description',
            new_name='bio',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='address',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='profile',
            name='location',
            field=models.CharField(max_length=30, blank=True),
        ),
    ]
