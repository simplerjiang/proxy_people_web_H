# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0030_auto_20180826_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='time_code',
            name='code',
            field=models.CharField(verbose_name='卡密', max_length=30, unique=True),
        ),
    ]
