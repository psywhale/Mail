# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-07-31 22:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Mail2', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mail',
            name='archived',
        ),
        migrations.AddField(
            model_name='mail',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Mail2.Mail'),
        ),
        migrations.AddField(
            model_name='route',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]