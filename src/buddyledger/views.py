from django.shortcuts import render
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
    except ledger.DoesNotExist:
        response = render_to_response('ledgerdoesnotexist.html')
        return response
    
    ### get all people related to this ledger
    people = Person.objects.filter(ledger_id=ledgerid)
    return render(request, 'showledger.html', {
        'ledger': ledger,
        'people': people
    })


def EditLedger(request, ledgerid=0):
    ### Check if the ledger exists - bail out if not
    try:
        ledger = Ledger.objects.get(pk = ledgerid)
    except ledger.DoesNotExist:
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


def AddPerson(request,ledgerid):
    if request.method == 'POST': # If the form has been submitted...
        form = PersonForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            person = form.save() # save the new person
            return HttpResponseRedirect('/ledger/%s' % ledgerid) # return to the ledger page
    else:
        form = PersonForm()

    return render(request, 'addperson.html', {
        'form': form,
    })
