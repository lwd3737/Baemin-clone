# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-10-13 18:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_shopdesc_intro_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='shop',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shop.Shop'),
        ),
    ]
