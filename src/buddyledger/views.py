from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from buddyledger.forms import LedgerForm, PersonForm, ExpenseForm, PaymentForm
from buddyledger.models import Ledger, Person, Expense, Payment, Currency
#from paymentprocessor import PaymentProcessor, MonoPayment

def CreateLedger(request):
    if request.method == 'POST':
        form = LedgerForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            ledger = Ledger(name=form['name'].data,currency_id=form['currency'].data)
            ledger.save()
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
    expenses = Expense.objects.filter(ledger_id=ledgerid)
    
    ### get all payments related to one of the expenses
    payments = Payment.objects.filter(expense_id__in=expenses)
    
    ### put the data structure for calculation together
    internaldata = []
    for expense in expenses:
        expensepayments = Payment.objects.filter(expense_id = expense.id)
        paymentlist = []
        for payment in expensepayments:
            paymentlist.append(dict(amount=payment.amount_native,user=payment.person.id))
        expensepeople = []
        for person in expense.people.all():
            expensepeople.append(person.id)
        internaldata.append(dict(payments=paymentlist,users=expensepeople))
    
    ### get calculated result
    #pp = PaymentProcessor(internaldata)
    
    
    ### render and return response
    return render(request, 'showledger.html', {
        'ledger': ledger,
        'people': people,
        'expenses': expenses,
        'payments': payments,
        'internaldata': internaldata
    })


def EditLedger(request, ledgerid=0):
    ### Check if the ledger exists - bail out if not
    try:
        ledger = Ledger.objects.get(pk = ledgerid)
    except Ledger.DoesNotExist:
        response = render_to_response('ledgerdoesnotexist.html')
        return response

    if request.method == 'POST':
        form = LedgerForm(request.POST) # A form bound to the ledger data
        if form.is_valid(): # All validation rules pass
            ledger.name = form['name'].data
            ledger.currency_id = form['currency'].data
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

    if request.method == 'POST':
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

    if request.method == 'POST':
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
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            expense = Expense(ledger_id=ledgerid,name=form['name'].data,amount=float(form['amount'].data),amount_native=ConvertCurrency(float(form['amount'].data),form['currency'].data,ledger.currency.id),currency_id=form['currency'].data)
            expense.save() # save the new expense
            for personid in form['people'].data:
                person = Person.objects.get(pk = personid)
                expense.people.add(person)
            return HttpResponseRedirect('/ledger/%s' % ledgerid) # return to the ledger page
        else:
            form = ExpenseForm(request.POST)
    else:
        form = ExpenseForm()
    
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
            expense.amount = float(form['amount'].data)
            expense.amount_native=ConvertCurrency(float(form['amount'].data),form['currency'].data,ledger.currency.id)
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
            payment = Payment(expense=expense,person=person,currency=currency,amount=float(form['amount'].data),amount_native=ConvertCurrency(float(form['amount'].data),form['currency'].data,expense.ledger.currency.id))
            payment.save() # save the new payment
            return HttpResponseRedirect('/ledger/%s' % expense.ledger.id) # return to the ledger page
        else:
            form = PaymentForm(request.POST)
    else:
        form = PaymentForm()

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
            payment.amount = float(form['amount'].data)
            payment.amount_native=ConvertCurrency(float(form['amount'].data),form['currency'].data,payment.expense.ledger.currency.id)
            payment.currency = payment.expense.currency
            payment.save()
            return HttpResponseRedirect('/ledger/%s' % payment.expense.ledger.id) # return to the ledger page
        else:
            form = PaymentForm(request.POST)
    else:
        form = PaymentForm(instance=payment)

    return render(request, 'editpayment.html', {
        'form': form,
        'payment': payment
    })


def RemovePayment(request, payment=0):
    ### Check if the payment exists - bail out if not
    try:
        payment = Payment.objects.get(pk = paymentid)
    except Paymet.DoesNotExist:
        response = render_to_response('paymentdoesnotexist.html')
        return response

    ledgerid = payment.expense.ledger.id
    payment.delete()
    return HttpResponseRedirect('/ledger/%s' % ledgerid) # return to the ledger page


def ConvertCurrency(amount,fromcurrencyid,tocurrencyid):
    fromcurrency = Currency.objects.get(pk=fromcurrencyid)
    tocurrency = Currency.objects.get(pk=tocurrencyid)
    ### first convert to DKK
    dkkamount = amount*fromcurrency.dkk_price
    ### convert to tocurrency
    returnamount = dkkamount / tocurrency.dkk_price
    return returnamount
