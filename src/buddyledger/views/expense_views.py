from decimal import *

from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response

from buddyledger.models import Ledger, Person, Expense, Payment, Currency
from buddyledger.forms import LedgerForm, PersonForm, ExpenseForm, PaymentForm

from buddyledger.views.misc import ConvertCurrency

def AddExpense(request, ledgerid=0):
    ### check if the ledger exists, bail out if not
    try:
        ledger = Ledger.objects.get(pk = ledgerid)
    except Ledger.DoesNotExist:
        response = render_to_response('ledgerdoesnotexist.html')
        return response
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            expense = Expense(ledger_id=ledgerid,name=form['name'].data,amount=Decimal(form['amount'].data),amount_native=ConvertCurrency(Decimal(form['amount'].data),form['currency'].data,ledger.currency.id),currency_id=form['currency'].data)
            expense.save() # save the new expense
            for personid in form['people'].data:
                person = Person.objects.get(pk = personid)
                expense.people.add(person)
            return HttpResponseRedirect('/expense/%s/addpayment/' % expense.id) # go straight to add expense page
        else:
            form = ExpenseForm(request.POST)
    else:
        form = ExpenseForm(initial={'currency': ledger.currency.id})
    
    form.fields["people"].queryset = Person.objects.filter(ledger_id=ledgerid)
    return render(request, 'addexpense.html', {
        'form': form,
    })


def EditExpense(request, expenseid=0):
    ### Check if the expense exists - bail out if not
    try:
        expense = Expense.objects.get(pk = expenseid)
    except Expense.DoesNotExist:
        response = render_to_response('expensedoesnotexist.html')
        return response

    if request.method == 'POST':
        form = ExpenseForm(request.POST) # A form bound to the expense data
        if form.is_valid(): # All validation rules pass
            expense.name = form['name'].data
            expense.amount = Decimal(form['amount'].data)
            expense.amount_native=ConvertCurrency(Decimal(form['amount'].data),form['currency'].data,expense.ledger.currency.id)
            currency = Currency.objects.get(pk = form['currency'].data)
            expense.currency = currency
            expense.save()
            expense.people.clear()
            for personid in form['people'].data:
                person = Person.objects.get(pk = personid)
                expense.people.add(person)
            return HttpResponseRedirect('/ledger/%s' % expense.ledger.id) # return to the ledger page
        else:
            form = ExpenseForm(request.POST)
    else:
        form = ExpenseForm(instance=expense)
    
    form.fields["people"].queryset = Person.objects.filter(ledger_id=expense.ledger.id)
    return render(request, 'editexpense.html', {
        'form': form,
        'expense': expense
    })


def RemoveExpense(request, expenseid=0):
    ### Check if the expense exists - bail out if not
    try:
        expense = Expense.objects.get(pk = expenseid)
    except Expense.DoesNotExist:
        response = render_to_response('expensedoesnotexist.html')
        return response

    ledgerid = expense.ledger.id
    expense.delete()
    return HttpResponseRedirect('/ledger/%s' % ledgerid) # return to the ledger page


def ExpenseAddPerson(request, expenseid=0, personid=0):
    ### Check if the expense exists - bail out if not
    try:
        expense = Expense.objects.get(pk = expenseid)
    except Expense.DoesNotExist:
        response = render_to_response('expensedoesnotexist.html')
        return response

    ### Check if the person exists - bail out if not
    try:
        person = Person.objects.get(pk = personid)
    except Person.DoesNotExist:
        response = render_to_response('persondoesnotexist.html')
        return response

    ### add this person to this expense
    expense.people.add(person)
    return HttpResponseRedirect('/ledger/%s' % expense.ledger.id) # return to the ledger page


def ExpenseRemovePerson(request, expenseid=0, personid=0):
    ### Check if the expense exists - bail out if not
    try:
        expense = Expense.objects.get(pk = expenseid)
    except Expense.DoesNotExist:
        response = render_to_response('expensedoesnotexist.html')
        return response

    ### Check if the person exists - bail out if not
    try:
        person = Person.objects.get(pk = personid)
    except Person.DoesNotExist:
        response = render_to_response('persondoesnotexist.html')
        return response

    ### remove this person from this expense
    expense.people.remove(person)
    return HttpResponseRedirect('/ledger/%s' % expense.ledger.id) # return to the ledger page
