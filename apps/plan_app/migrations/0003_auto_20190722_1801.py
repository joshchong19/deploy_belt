# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-07-22 18:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan_app', '0002_auto_20190722_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trips',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='trips',
            name='start_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='users',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]