# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-09-15 05:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20180915_1420'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shopdesc',
            old_name='finisehd_time',
            new_name='finised_time',
        ),
    ]
