# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-26 09:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='editor',
            field=models.ManyToManyField(to='books.Editor'),
        ),
    ]