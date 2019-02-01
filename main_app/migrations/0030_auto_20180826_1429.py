# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0029_getmoney_account_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='software',
            name='software_cost',
            field=models.DecimalField(verbose_name='价格', default=0, max_digits=8, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='software',
            name='software_each_time',
            field=models.PositiveIntegerField(verbose_name='套餐时间（按天计算）', default=720),
        ),
        migrations.AlterField(
            model_name='software',
            name='software_id',
            field=models.PositiveIntegerField(verbose_name='会员ID', unique=True),
        ),
        migrations.AlterField(
            model_name='software',
            name='software_name',
            field=models.CharField(verbose_name='会员名称', max_length=30),
        ),
        migrations.AlterField(
            model_name='software',
            name='software_try',
            field=models.BooleanField(verbose_name='试用（无需填写，默认即可）', default=False),
        ),
        migrations.AlterField(
            model_name='software',
            name='software_try_hours',
            field=models.PositiveIntegerField(verbose_name='试用时长（无需填写，默认即可）', default=0),
        ),
        migrations.AlterField(
            model_name='software',
            name='software_version_number',
            field=models.CharField(verbose_name='会员版本号', max_length=30, default='V1.0'),
        ),
        migrations.AlterField(
            model_name='time_code',
            name='begin_time',
            field=models.DateTimeField(verbose_name='存卡时间', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='time_code',
            name='code',
            field=models.CharField(verbose_name='卡密', max_length=30),
        ),
        migrations.AlterField(
            model_name='time_code',
            name='deal_object',
            field=models.ForeignKey(verbose_name='交易订单', null=True, to='main_app.Deal_record'),
        ),
        migrations.AlterField(
            model_name='time_code',
            name='proxy_man',
            field=models.ForeignKey(verbose_name='购卡代理', null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='time_code',
            name='software',
            field=models.ForeignKey(verbose_name='会员对象', to='main_app.Software'),
        ),
    ]
