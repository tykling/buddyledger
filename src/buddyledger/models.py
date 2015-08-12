from django.db import models

class Ledger(models.Model):
    name = models.CharField(max_length=100)
    currency = models.ForeignKey('Currency')
    closed = models.BooleanField(default=False,editable=False)
    calcmethod = models.CharField(max_length=20,editable=False,default="basic")
    
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
    amount_native = models.DecimalField(max_digits=20, decimal_places=2, editable=False)
    ledger = models.ForeignKey('Ledger',editable=False)
    people = models.ManyToManyField('Person', through='ExpensePart')
    date = models.DateField()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('date','id',)


class ExpensePart(models.Model):
    expense = models.ForeignKey(Expense)
    person = models.ForeignKey(Person)
    haspaid = models.DecimalField(max_digits=20, decimal_places=2,null=True,blank=True)
    haspaid_native = models.DecimalField(max_digits=20, decimal_places=2,null=True,blank=True)
    shouldpay = models.DecimalField(max_digits=20, decimal_places=2,null=True,blank=True)
    shouldpay_native = models.DecimalField(max_digits=20, decimal_places=2,null=True,blank=True)


class Currency(models.Model):
    iso4217_code = models.CharField(max_length=3)
    dkk_price = models.DecimalField(max_digits=20, decimal_places=2)
    
    def __unicode__(self):
        return self.iso4217_code
    
    class Meta:
        ordering = ('iso4217_code',)
