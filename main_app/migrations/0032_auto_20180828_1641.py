# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0031_auto_20180826_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='others_info',
            name='TOKEN',
            field=models.CharField(verbose_name='API密链', max_length=15, default='O9d8n1X7i6V1b4'),
        ),
        migrations.AlterField(
            model_name='others_info',
            name='ad',
            field=models.CharField(verbose_name='代理广告', max_length=30, default='z1v6I9N2N0i1G3'),
        ),
    ]
