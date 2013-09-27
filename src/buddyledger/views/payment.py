from decimal import *

from buddyledger.forms import LedgerForm, PersonForm, ExpenseForm, PaymentForm
from buddyledger.models import Ledger, Person, Expense, Payment, Currency

from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect

from buddyledger.views.misc import ConvertCurrency

def AddPayment(request, expenseid=0):
    ### Check if the expense exists - bail out if not
    try:
        expense = Expense.objects.get(pk = expenseid)
    except Expense.DoesNotExist:
        response = render_to_response('expensedoesnotexist.html')
        return response
    
    if request.method == 'POST':
        form = PaymentForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            expense = Expense.objects.get(pk = expenseid)
            person = Person.objects.get(pk = form['person'].data)
            currency = expense.currency
            payment = Payment(expense=expense,person=person,currency=currency,amount=Decimal(form['amount'].data),amount_native=ConvertCurrency(Decimal(form['amount'].data),expense.currency.id,expense.ledger.currency.id))
            payment.save() # save the new payment
            return HttpResponseRedirect('/ledger/%s' % expense.ledger.id) # return to the ledger page
        else:
            form = PaymentForm(request.POST)
    else:
        form = PaymentForm(initial={'amount': expense.amount})
    
    form.fields["person"].queryset = Person.objects.filter(ledger_id=expense.ledger.id)
    return render(request, 'addpayment.html', {
        'form': form,
        'expense': expense
    })


def EditPayment(request, paymentid=0):
    ### Check if the payment exists - bail out if not
    try:
        payment = Payment.objects.get(pk = paymentid)
    except Payment.DoesNotExist:
        response = render_to_response('paymentdoesnotexist.html')
        return response

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid(): # All validation rules pass
            payment.person = Person.objects.get(pk = form['person'].data)
            payment.amount = Decimal(form['amount'].data)
            ### convert to native currency for this ledger
            payment.amount_native=ConvertCurrency(Decimal(form['amount'].data),payment.expense.currency.id,payment.expense.ledger.currency.id)
            payment.currency = payment.expense.currency
            payment.save()
            return HttpResponseRedirect('/ledger/%s' % payment.expense.ledger.id) # return to the ledger page
        else:
            form = PaymentForm(request.POST)
    else:
        form = PaymentForm(instance=payment)

    form.fields["person"].queryset = Person.objects.filter(ledger_id=expense.ledger.id)
    return render(request, 'editpayment.html', {
        'form': form,
        'payment': payment
    })


def RemovePayment(request, paymentid=0):
    ### Check if the payment exists - bail out if not
    try:
        payment = Payment.objects.get(pk = paymentid)
    except Payment.DoesNotExist:
        response = render_to_response('paymentdoesnotexist.html')
        return response

    ledgerid = payment.expense.ledger.id
    payment.delete()
    return HttpResponseRedirect('/ledger/%s' % ledgerid) # return to the ledger page
