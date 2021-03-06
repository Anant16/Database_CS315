# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-16 07:56
from __future__ import unicode_literals

import datetime
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
            name='Historical',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField()),
                ('Open', models.FloatField()),
                ('High', models.FloatField()),
                ('Low', models.FloatField()),
                ('Close', models.FloatField()),
                ('Volume', models.FloatField()),
                ('Adj_Close', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=100, verbose_name='Symbol')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SymbolInfo',
            fields=[
                ('Handle', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=100)),
                ('Exchange', models.CharField(max_length=10)),
                ('Country', models.CharField(max_length=50)),
                ('DateStamp', models.DateField(default=datetime.datetime(1960, 3, 12, 0, 0))),
            ],
        ),
        migrations.AddField(
            model_name='historical',
            name='Handle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.SymbolInfo'),
        ),
        migrations.AlterUniqueTogether(
            name='historical',
            unique_together=set([('Handle', 'Date')]),
        ),
    ]
