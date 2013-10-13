from decimal import *

from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.forms.models import inlineformset_factory

from buddyledger.models import Ledger, Person, Expense, Currency, ExpensePart
from buddyledger.forms import LedgerForm, PersonForm, ExpenseForm

from buddyledger.views.misc import ConvertCurrency

def AddExpense(request, ledgerid=0):
    ### check if the ledger exists, bail out if not
    try:
        ledger = Ledger.objects.get(pk = ledgerid)
    except Ledger.DoesNotExist:
        response = render_to_response('ledgerdoesnotexist.html')
        return response
    
    ### get all people associated with this ledger
    people = Person.objects.filter(ledger_id=ledgerid).order_by('name')
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST,people=people)
        if form.is_valid(): # All validation rules pass
            expense = Expense(ledger_id=ledgerid,name=form['name'].data,amount=Decimal(form['amount'].data),amount_native=ConvertCurrency(Decimal(form['amount'].data),form['currency'].data,ledger.currency.id),currency_id=form['currency'].data)
            
            ### loop through the expenseparts
            expenseparts = dict()
            for (uid,shouldpay,haspaid) in form.get_expense_parts():
                if haspaid == '':
                    haspaid = 0
                if shouldpay == '':
                    shouldpay = 0
                expenseparts[uid] = dict(shouldpay=shouldpay,haspaid=haspaid)
            
            ### calculate customtotal and autocount
            customtotal = 0
            autocount = 0
            paymenttotal = 0
            for uid,temp in expenseparts.iteritems():
                if temp['shouldpay'] != "auto":
                    customtotal += temp['shouldpay']
                else:
                    autocount += 1
            
                try:
                    paymenttotal += Decimal(temp['haspaid'])
                except Exception as e:
                    response = render_to_response('invalidexpense.html')
                    return response                
            
            ### find the splitpart
            remaining = expense.amount - customtotal
            if remaining > 0:
                splitpart = remaining / autocount
            
            ### check if customtotal + remaining = expense amount
            if expense.amount != customtotal + remaining:
                ### error, bail out
                response = render_to_response('invalidexpense.html')
                return response
            
            ### check if the the payments add up to the expense amount
            if expense.amount != paymenttotal:
                ### error, bail out
                response = render_to_response('invalidexpense.html')
                return response
            
            ### OK, save the expense
            expense.save() # save the new expense
                
            ### loop through the expenseparts again and save each
            for uid,temp in expenseparts.iteritems():
                if temp['shouldpay'] != "auto":
                    expensepart = ExpensePart.objects.create(person_id=uid,expense_id=expense.id,shouldpay=temp['shouldpay'],haspaid=temp['haspaid'])
                else:
                    expensepart = ExpensePart.objects.create(person_id=uid,expense_id=expense.id,shouldpay=splitpart,haspaid=temp['haspaid'])
                expensepart.save()
            
            ### return to the ledger page, expense tab
            return HttpResponseRedirect('/ledger/%s/#expenses' % ledgerid)
        else:
            ### form not valid
            form = ExpenseForm(request.POST,people=people)
    else:
        ### page not POSTed
        form = ExpenseForm(initial={'currency': ledger.currency.id},people=people)
        
    return render(request, 'addexpense.html', {
        'form': form,
        'people': people,
        'ledger': ledger
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
