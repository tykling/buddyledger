# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('iso4217_code', models.CharField(max_length=3)),
                ('dkk_price', models.DecimalField(max_digits=20, decimal_places=2)),
            ],
            options={
                'ordering': ('iso4217_code',),
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('amount', models.DecimalField(max_digits=20, decimal_places=2)),
                ('amount_native', models.DecimalField(editable=False, max_digits=20, decimal_places=2)),
                ('date', models.DateField()),
                ('currency', models.ForeignKey(to='buddyledger.Currency')),
            ],
            options={
                'ordering': ('date', 'id'),
            },
        ),
        migrations.CreateModel(
            name='ExpensePart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('haspaid', models.DecimalField(null=True, max_digits=20, decimal_places=2, blank=True)),
                ('haspaid_native', models.DecimalField(null=True, max_digits=20, decimal_places=2, blank=True)),
                ('shouldpay', models.DecimalField(null=True, max_digits=20, decimal_places=2, blank=True)),
                ('shouldpay_native', models.DecimalField(null=True, max_digits=20, decimal_places=2, blank=True)),
                ('expense', models.ForeignKey(to='buddyledger.Expense')),
            ],
        ),
        migrations.CreateModel(
            name='Ledger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('closed', models.BooleanField(default=False, editable=False)),
                ('calcmethod', models.CharField(default=b'basic', max_length=20, editable=False)),
                ('currency', models.ForeignKey(to='buddyledger.Currency')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('ledger', models.ForeignKey(editable=False, to='buddyledger.Ledger')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='expensepart',
            name='person',
            field=models.ForeignKey(to='buddyledger.Person'),
        ),
        migrations.AddField(
            model_name='expense',
            name='ledger',
            field=models.ForeignKey(editable=False, to='buddyledger.Ledger'),
        ),
        migrations.AddField(
            model_name='expense',
            name='people',
            field=models.ManyToManyField(to='buddyledger.Person', through='buddyledger.ExpensePart'),
        ),
    ]
