# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-12 08:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20170412_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='current_cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.Cart'),
        ),
    ]
