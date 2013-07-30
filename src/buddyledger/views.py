from django.shortcuts import render
from django.http import HttpResponseRedirect
from buddyledger.forms import LedgerForm, PersonForm, ExpenseForm, PaymentForm

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