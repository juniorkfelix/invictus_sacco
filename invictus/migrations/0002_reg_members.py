# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-02-14 15:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invictus', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='reg_members',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=100)),
                ('dob', models.DateField(max_length=50)),
                ('idno', models.IntegerField()),
                ('member_no', models.CharField(max_length=100)),
                ('mobile', models.IntegerField()),
                ('month_cont', models.IntegerField()),
                ('email', models.EmailField(max_length=20)),
                ('employer', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('county', models.CharField(max_length=50)),
                ('religion', models.CharField(max_length=50)),
                ('kin_fullname', models.CharField(max_length=100)),
                ('kin_phone', models.IntegerField()),
                ('kin_id', models.IntegerField()),
                ('kin_relation', models.CharField(max_length=70)),
                ('datestamp', models.DateField()),
                ('transaction_reference', models.CharField(max_length=80)),
            ],
        ),
    ]
