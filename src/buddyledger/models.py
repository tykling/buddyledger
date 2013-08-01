from django.db import models

class Ledger(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=100)
    ledger = models.ForeignKey(Ledger,editable=False)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ('name',)


class Expense(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.ForeignKey('Currency')
    ledger = models.ForeignKey('Ledger',editable=False)
    people = models.ManyToManyField('Person',null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('id',)

class Payment(models.Model):
    expense = models.ForeignKey('Expense',editable=False)
    person = models.ForeignKey('Person')
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.ForeignKey('Currency',editable=False)


class Currency(models.Model):
    iso4217_code = models.CharField(max_length=3)
    dkk_price_for_100 = models.DecimalField(max_digits=20, decimal_places=2)

    def __unicode__(self):
        return self.iso4217_code
    class Meta:
        ordering = ('iso4217_code',)