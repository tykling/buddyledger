from decimal import *

from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect

from buddyledger.forms import BackPaymentForm
from buddyledger.models import Ledger, Person, Expense, Currency, BackPayment

def AddBackPayment(request,payerid=0,receiverid=0):
    ### check if the payer and receiver exists, bail out if not
    try:
        payer = Person.objects.get(pk = payerid)
        receiver = Person.objects.get(pk = receiverid)
    except Ledger.DoesNotExist:
        response = render_to_response('backpayment_person_does_not_exist.html')
        return response

    ### check that the two persons are associated with the same ledger
    if payer.ledger != receiver.ledger:
        response = render_to_response('backpayment_person_wrong_ledger.html')
        return response
    else:
        ledgerid = payer.ledger.id
        ledger = Ledger.objects.get(pk = ledgerid)

    ### check the request method
    if request.method == 'POST':
        form = BackPaymentForm(request.POST)
        if form.is_valid():
            bp = BackPayment(ledger_id=ledgerid,payer=payer,receiver=receiver,amount=form['amount'].data,amount_native=ConvertCurrency(Decimal(form['amount'].data),form['currency'].data,ledger.currency.id),currency_id=form['currency'].data)
            bp.save()
            return HttpResponseRedirect('/ledger/%s/#backpayments' % ledgerid) # return to the ledger page, backpayments tab
        else:
            form = BackPaymentForm(request.POST)
    else:
        form = BackPaymentForm(initial={'currency': ledger.currency.id})

    return render(request, 'add_backpayment.html', {
        'form': form,
    })


def EditBackPayment(request, bpid=0):
    ### Check if the backpayment exists - bail out if not
    try:
        bp = BackPayment.objects.get(pk = bpid)
    except BackPayment.DoesNotExist:
        response = render_to_response('backpayment_does_not_exist.html')
        return response

    ### check the request method
    if request.method == 'POST':
        form = BackPaymentForm(request.POST)
        if form.is_valid():
            bp.amount = form['amount'].data
            bp.currency_id = form['currency'].data
            bp.amount_native=ConvertCurrency(Decimal(form['amount'].data),form['currency'].data,ledger.currency.id)
            bp.save()
            return HttpResponseRedirect('/ledger/%s/#backpayments' % bp.ledger.id)
        else:
            form = BackPaymentForm(request.POST)
    else:
        form = BackPaymentForm(instance=bp)

    return render(request, 'edit_backpayment.html', {
        'form': form,
        'bp': bp
    })


def RemoveBackPayment(request, bpid=0):    
    ### Check if the backpayment exists - bail out if not
    try:
        bp = BackPayment.objects.get(pk = bpid)
    except BackPayment.DoesNotExist:
        response = render_to_response('backpayment_does_not_exist.html')
        return response

    if request.method == 'POST':
        ledgerid = bp.ledger.id
        bp.delete()
        return HttpResponseRedirect('/ledger/%s/#backpayments' % ledgerid) # return to the ledger page, backpayments tab
    else:
        return render(request, 'confirm_backpayment_delete.html', {
            'form': DeleteBackPaymentForm(),
            'bp': bp
        })
