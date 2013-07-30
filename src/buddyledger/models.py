from django.db import models

class Ledger(models.Model):
    name = models.CharField(max_length=100)

class Person(models.Model):
    name = models.CharField(max_length=100)
    ledger = models.ForeignKey(Ledger)

class Expense(models.Model):
    name = models.CharField(max_length=100)
    amount = models.BigIntegerField()

class ExpensePerson(models.Model):
    expense = models.ForeignKey(Expense)
    person = models.ForeignKey(Person)

class Payment(models.Model):
    expense = models.ForeignKey(Expense)
    person = models.ForeignKey(Person)
    amount = models.BigIntegerField()
