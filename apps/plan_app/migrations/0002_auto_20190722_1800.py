# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-07-22 18:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='updated_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]
