# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-27 00:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0006_auto_20180426_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='zipcode',
            field=models.IntegerField(default=12345),
        ),
    ]
