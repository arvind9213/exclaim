# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-11 06:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_remove_post_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='SDF', unique=True),
            preserve_default=False,
        ),
    ]