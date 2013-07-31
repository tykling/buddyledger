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


class Expense(models.Model):
    name = models.CharField(max_length=100)
    amount = models.BigIntegerField()
    currency = models.ForeignKey(Currency)
    ledger = models.ForeignKey(Ledger,editable=False)
    
    def __unicode__(self):
        return self.name


class ExpensePerson(models.Model):
    expense = models.ForeignKey(Expense)
    person = models.ForeignKey(Person)


class Payment(models.Model):
    expense = models.ForeignKey(Expense)
    person = models.ForeignKey(Person)
    amount = models.BigIntegerField()
    currency = models.ForeignKey(Currency)


class Currency(models.Model):
    iso4217_code = models.CharField(max_length=3)
    danish_ore_price = models.BigIntegerField()