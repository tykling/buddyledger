from django.db import models

class Ledger(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=100)
    ledger = models.ForeignKey(Ledger)
    def __unicode__(self):
        return self.name

class Expense(models.Model):
    name = models.CharField(max_length=100)
    amount = models.BigIntegerField()
    
    def __unicode__(self):
        return self.name

class ExpensePerson(models.Model):
    expense = models.ForeignKey(Expense)
    person = models.ForeignKey(Person)

class Payment(models.Model):
    expense = models.ForeignKey(Expense)
    person = models.ForeignKey(Person)
    amount = models.BigIntegerField()
