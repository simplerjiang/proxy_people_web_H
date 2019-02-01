# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0032_auto_20180828_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='others_info',
            name='TOKEN',
            field=models.CharField(verbose_name='API密链', max_length=15, default='Y0W1I5n3W3k6B6'),
        ),
        migrations.AlterField(
            model_name='others_info',
            name='ad',
            field=models.CharField(verbose_name='代理广告', max_length=30, default='g9v2b7q7T2J4J3'),
        ),
    ]
