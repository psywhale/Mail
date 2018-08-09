# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-07-30 19:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filepath', models.CharField(max_length=512)),
                ('filename', models.CharField(max_length=1024)),
                ('hashedname', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('subject', models.CharField(max_length=512)),
                ('termcode', models.CharField(max_length=4)),
                ('section', models.CharField(max_length=5)),
                ('archived', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('fk_sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to', models.CharField(default='', max_length=300)),
                ('read', models.BooleanField(default=False)),
                ('fk_mail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mail2.Mail')),
            ],
        ),
        migrations.AddField(
            model_name='attachment',
            name='m2m_mail',
            field=models.ManyToManyField(to='Mail2.Mail'),
        ),
    ]
