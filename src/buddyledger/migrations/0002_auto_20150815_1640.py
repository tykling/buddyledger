# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buddyledger', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expensepart',
            name='autoamount',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='expensepart',
            name='expense',
            field=models.ForeignKey(related_name='expenseparts', to='buddyledger.Expense'),
        ),
        migrations.AlterField(
            model_name='expensepart',
            name='person',
            field=models.ForeignKey(to='buddyledger.Person', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='ledger',
            name='calcmethod',
            field=models.CharField(default=b'basic', max_length=20, editable=False),
        ),
        migrations.AlterUniqueTogether(
            name='expensepart',
            unique_together=set([('expense', 'person')]),
        ),
    ]
