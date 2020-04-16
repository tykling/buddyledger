from decimal import *
import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.forms.models import inlineformset_factory
from django.views.generic.edit import DeleteView

from buddyledger.models import Ledger, Person, Expense, Currency, ExpensePart
from buddyledger.forms import LedgerForm, PersonForm, ExpenseForm, DeleteExpenseForm

from buddyledger.views.misc import ConvertCurrency, render_to_response

def ValidateExpense(customtotal, splitpart, autocount, remainder, expense, paymenttotal):
    ### check if customtotal + remaining = expense amount
    if customtotal + (splitpart*autocount) + remainder != expense.amount:
        return False
    
    ### check if the the payments add up to the expense amount
    if expense.amount != paymenttotal:
        return False
    
    ### all good
    return True


def GetTotals(expenseparts):
    ### calculate customtotal, paymenttotal and autocount
    customtotal = 0
    autocount = 0
    paymenttotal = 0
    for uid,temp in expenseparts.items():
        if temp['shouldpay'] != "auto":
            customtotal += Decimal(temp['shouldpay'])
        else:
            autocount += 1

        try:
            paymenttotal += Decimal(temp['haspaid'])
        except Exception as e:
            return False
    return customtotal, autocount, paymenttotal


def GetSplitParts(expense, customtotal, autocount):
    ### find the splitpart
    remaining = expense.amount - customtotal
    remainder = 0
    splitpart = 0
    if remaining > 0:
        splitpart = Decimal(remaining / autocount).quantize(Decimal('.01'), rounding=ROUND_DOWN)
        remainder = Decimal((expense.amount-customtotal) - Decimal(splitpart * autocount))
    return splitpart, remainder


def CreateExpenseParts(expenseparts, expense, ledger, splitpart, remainder):
    for uid,temp in expenseparts.items():
        if temp['shouldpay'] != "auto":
            expensepart = ExpensePart.objects.create(
                person_id=uid,
                expense_id=expense.id,
                shouldpay=temp['shouldpay'],
                shouldpay_native=ConvertCurrency(temp['shouldpay'], expense.currency.id, ledger.currency.id),
                haspaid=temp['haspaid'],
                haspaid_native=ConvertCurrency(temp['haspaid'], expense.currency.id, ledger.currency.id),
                autoamount=False
            )
        else:
            expensepart = ExpensePart.objects.create(
                person_id=uid,
                expense_id=expense.id,
                shouldpay=splitpart+remainder,
                shouldpay_native=ConvertCurrency(splitpart+remainder, expense.currency.id, ledger.currency.id),
                haspaid=temp['haspaid'],
                haspaid_native=ConvertCurrency(temp['haspaid'], expense.currency.id, ledger.currency.id),
                autoamount=True
            )
            remainder = 0
        expensepart.save()


def AddExpense(request, ledgerid=0):
    ### check if the ledger exists, bail out if not
    try:
        ledger = Ledger.objects.get(pk = ledgerid)
    except Ledger.DoesNotExist:
        response = render_to_response(request, 'ledgerdoesnotexist.html')
        return response

    ### check if the ledger is open
    if ledger.closed:
        response = render_to_response(request, 'ledger_is_closed.html')
        return response

    ### get all people associated with this ledger
    people = Person.objects.filter(ledger_id=ledgerid).order_by('name')
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST, people=people)
        if form.is_valid(): # All validation rules pass
            expense = Expense(
                ledger_id=ledgerid,
                name=form['name'].data,
                amount=Decimal(form['amount'].data),
                amount_native=ConvertCurrency(Decimal(form['amount'].data),
                form['currency'].data,
                ledger.currency.id),
                currency_id=form['currency'].data,
                date=form['date'].data
            )
            
            ### get the expenseparts
            expenseparts = form.get_expense_parts()
            
            ### get totals
            totals = GetTotals(expenseparts)
            if not totals:
                return render_to_response(request, 'invalid_expense.html')
            customtotal, autocount, paymenttotal = totals
            
            ### get splitpart (and remainder if any)
            splitpart, remainder = GetSplitParts(expense, customtotal, autocount)
            
            ### validate ledger
            if not ValidateExpense(customtotal, splitpart, autocount, remainder, expense, paymenttotal):
                return render_to_response(request, 'invalid_expense.html')
            
            ### OK, save the expense
            expense.save() # save the new expense
                
            ### loop through the expenseparts again and save each
            CreateExpenseParts(expenseparts, expense, ledger, splitpart, remainder)
            
            ### return to the ledger page, expense tab
            return HttpResponseRedirect('/ledger/%s/#expenses' % ledger.id)
        else:
            ### form not valid
            form = ExpenseForm(request.POST, people=people)
    else:
        ### page not POSTed
        form = ExpenseForm(
            initial={'currency': ledger.currency.id, 'date': datetime.date.today}, 
            people=people
        )

    return render(request, 'add_expense.html', {
        'form': form,
        'people': people,
        'ledger': ledger
    })

def EditExpense(request, expenseid=0):
    ### Check if the expense exists - bail out if not
    try:
        expense = Expense.objects.get(pk = expenseid)
    except Expense.DoesNotExist:
        response = render_to_response(request, 'expense_does_not_exist.html')
        return response

    ### check if the ledger is open
    if expense.ledger.closed:
        response = render_to_response(request, 'ledger_is_closed.html')
        return response

    ### get all people associated with this ledger
    people = Person.objects.filter(ledger=expense.ledger).order_by('name')
    
    ### get all people associated with this expense
    expensepeople = Person.objects.filter(expense=expense).order_by('name')

    form = ExpenseForm(request.POST or None, people=people, expenseparts=expense.expenseparts.all(), initial={
        'name': expense.name, 
        'amount': expense.amount,
        'currency': expense.currency.id,
        'date': expense.date,
    })
    if form.is_valid(): # All validation rules pass
        expense.name = form['name'].data
        expense.amount = Decimal(form['amount'].data)
        expense.amount_native=ConvertCurrency(Decimal(form['amount'].data),form['currency'].data,expense.ledger.currency.id)
        expense.currency = Currency.objects.get(pk = form['currency'].data)

        ### get the expenseparts
        expenseparts = form.get_expense_parts()

        ### get totals
        totals = GetTotals(expenseparts)
        if not totals:
            return render_to_response(request, 'invalid_expense.html')
        customtotal, autocount, paymenttotal = totals
        
        ### get splitpart (and remainder if any)
        splitpart, remainder = GetSplitParts(expense, customtotal, autocount)
        
        ### validate expense
        if not ValidateExpense(customtotal, splitpart, autocount, remainder, expense, paymenttotal):
            return render_to_response(request, 'invalid_expense.html')
        
        ### OK, save the expense
        expense.save() # save the expense
            
        ### loop through the expenseparts again and save each
        for ep in expense.expenseparts.all():
            ep.delete()
        CreateExpenseParts(expenseparts, expense, expense.ledger, splitpart, remainder)
        
        ### return response
        return HttpResponseRedirect('/ledger/%s/#expenses' % expense.ledger.id)
    
    return render(request, 'edit_expense.html', {
        'form': form,
        'expense': expense,
        'people': people,
        'expensepeople': expensepeople,
        'expenseparts': expense.expenseparts.all(),
    })


def RemoveExpense(request, expenseid=0):
    ### Check if the expense exists - bail out if not
    try:
        expense = Expense.objects.get(pk = expenseid)
    except Expense.DoesNotExist:
        response = render_to_response(request, 'expense_does_not_exist.html')
        return response

    ### check if the ledger is open
    if expense.ledger.closed:
        response = render_to_response(request, 'ledger_is_closed.html')
        return response

    if request.method == 'POST':
        ledgerid = expense.ledger.id
        expense.delete()
        return HttpResponseRedirect('/ledger/%s/#expenses' % ledgerid) # return to the ledger page, expenses tab
    else:
        return render(request, 'confirm_expense_delete.html', {
            'form': DeleteExpenseForm(),
            'expense': expense
        })


def ExpenseAddPerson(request, expenseid=0, personid=0):
    pass


def ExpenseRemovePerson(request, expenseid=0, personid=0):
    pass
