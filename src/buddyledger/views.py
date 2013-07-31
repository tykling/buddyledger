from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from buddyledger.forms import LedgerForm, PersonForm, ExpenseForm, PaymentForm
from buddyledger.models import Ledger, Person, Expense, ExpensePerson, Payment

def CreateLedger(request):
    if request.method == 'POST': # If the form has been submitted...
        form = LedgerForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            ledger = form.save() # save the new ledger
            return HttpResponseRedirect('/ledger/%s' % ledger.id) # return to the ledger page
    else:
        form = LedgerForm()

    return render(request, 'createledger.html', {
        'form': form,
    })


def ShowLedger(request, ledgerid=0):
    ### Check if the ledger exists - bail out if not
    try:
        ledger = Ledger.objects.get(pk = ledgerid)
    except Ledger.DoesNotExist:
        response = render_to_response('ledgerdoesnotexist.html')
        return response
    
    ### get all people related to this ledger
    people = Person.objects.filter(ledger_id=ledgerid)
    
    ### get all expenses related to this ledger
    ledgers = Expense.objects.filter(ledger_id=ledgerid)
    
    ### render and return response
    return render(request, 'showledger.html', {
        'ledger': ledger,
        'people': people,
        'ledgers': ledgers
    })


def EditLedger(request, ledgerid=0):
    ### Check if the ledger exists - bail out if not
    try:
        ledger = Ledger.objects.get(pk = ledgerid)
    except Ledger.DoesNotExist:
        response = render_to_response('ledgerdoesnotexist.html')
        return response

    if request.method == 'POST': # If the form has been submitted...
        form = LedgerForm(request.POST) # A form bound to the ledger data
        if form.is_valid(): # All validation rules pass
            ledger.name = form['name'].data
            ledger.save()
            return HttpResponseRedirect('/ledger/%s' % ledger.id) # return to the ledger page
        else:
            form = LedgerForm(request.POST)
    else:
        form = LedgerForm(instance=ledger)

    return render(request, 'editledger.html', {
        'form': form,
        'ledgerid': ledgerid
    })


def AddPerson(request,ledgerid=0):
    ### check if the ledger exists, bail out if not
    try:
        ledger = Ledger.objects.get(pk = ledgerid)
    except Ledger.DoesNotExist:
        response = render_to_response('ledgerdoesnotexist.html')
        return response

    if request.method == 'POST': # If the form has been submitted...
        form = PersonForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            person = Person(ledger_id=ledgerid,name=form['name'].data)
            person.save() # save the new person
            return HttpResponseRedirect('/ledger/%s' % ledgerid) # return to the ledger page
        else:
            form = PersonForm(request.POST)
    else:
        form = PersonForm()

    return render(request, 'addperson.html', {
        'form': form,
    })


def EditPerson(request, personid=0):
    ### Check if the person exists - bail out if not
    try:
        person = Person.objects.get(pk = personid)
    except Person.DoesNotExist:
        response = render_to_response('persondoesnotexist.html')
        return response

    if request.method == 'POST': # If the form has been submitted...
        form = LedgerForm(request.POST) # A form bound to the person data
        if form.is_valid(): # All validation rules pass
            person.name = form['name'].data
            person.save()
            return HttpResponseRedirect('/ledger/%s' % person.ledger.id) # return to the ledger page
        else:
            form = PersonForm(request.POST)
    else:
        form = PersonForm(instance=person)

    return render(request, 'editperson.html', {
        'form': form,
        'person': person
    })


def RemovePerson(request, personid=0):
    ### Check if the person exists - bail out if not
    try:
        person = Person.objects.get(pk = personid)
    except Person.DoesNotExist:
        response = render_to_response('persondoesnotexist.html')
        return response

    ledgerid = person.ledger.id
    person.delete()
    return HttpResponseRedirect('/ledger/%s' % ledgerid) # return to the ledger page


def AddExpense(request, ledgerid=0):
    ### check if the ledger exists, bail out if not
    try:
        ledger = Ledger.objects.get(pk = ledgerid)
    except Ledger.DoesNotExist:
        response = render_to_response('ledgerdoesnotexist.html')
        return response
    
    if request.method == 'POST': # If the form has been submitted...
        form = ExpenseForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            expense = Expense(ledger_id=ledgerid,name=form['name'].data,amount=form['amount'].data)
            expense.save() # save the new expense
            return HttpResponseRedirect('/ledger/%s' % ledgerid) # return to the ledger page
        else:
            form = ExpenseForm(request.POST)
    else:
        form = ExpenseForm()

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

    if request.method == 'POST': # If the form has been submitted...
        form = ExpenseForm(request.POST) # A form bound to the expense data
        if form.is_valid(): # All validation rules pass
            expense.name = form['name'].data
            expense.amount = form['amount'].data
            expense.save()
            return HttpResponseRedirect('/ledger/%s' % expense.ledger.id) # return to the ledger page
        else:
            form = ExpenseForm(request.POST)
    else:
        form = ExpenseForm(instance=expense)

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
