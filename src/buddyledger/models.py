from django.db import models

class Ledger(models.Model):
    name = models.TextField()

class Person(models.Model):
    name = models.TextField()
    ledger = models.ForeignKey(Ledger)

class Expense(models.Model):
    name = models.TextField()
    amount = models.BigIntegerField()

class ExpensePerson(models.Model):
    expense = models.ForeignKey(Expense)
    person = models.ForeignKey(Person)

class Payment(models.Model):
    expense = models.ForeignKey(Expense)
    person = models.ForeignKey(Person)
    amount = models.BigIntegerField()
