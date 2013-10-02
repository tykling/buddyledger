from decimal import *

from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.forms.models import inlineformset_factory

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
    
    people = Person.objects.filter(ledger_id=ledgerid)
    if request.method == 'POST':
        form = ExpenseForm(request.POST,people=people)
        if form.is_valid(): # All validation rules pass
            expense = Expense(ledger_id=ledgerid,name=form['name'].data,amount=Decimal(form['amount'].data),amount_native=ConvertCurrency(Decimal(form['amount'].data),form['currency'].data,ledger.currency.id),currency_id=form['currency'].data)
            expense.save() # save the new expense
            for (uid,amount) in form.get_expense_parts():
                ExpensePart.objects.create(person_id=uid,expense_id=expense.id,amount=amount)
            return HttpResponseRedirect('/expense/%s/addpayment/' % expense.id) # go straight to add payment page after save
        else:
            form = ExpenseForm(request.POST,people=people)
    else:
        form = ExpenseForm(initial={'currency': ledger.currency.id},people=people)
    
    customexpenseform = []
    for person in people:
        temp = """
<tr>
    <td>%s</td>
    <td>
        <div id="animated-switch" class="make-switch switch-small" data-animated="false" data-on="success" data-off="danger" data-on-label="Pay" data-off-label="Not">
            <input id="expensepart_%s" name="person_expensepart_%s" type="checkbox" />
        </div>
    </td>
    <td>
        <div id="animated-switch" class="make-switch switch-small" data-animated="false" data-on="default" data-off="primary" data-on-label="Auto" data-off-label="Custom">
            <input id="autoamount_%s" name="person_autoamount_%s" type="checkbox" disabled />
        </div>
    </td>
    <td>
        <input id="customamount_%s" name="person_customamount_%s" type="text" disabled />
    </td>
</tr>
<script>
    $('#expensepart_%s').on('switch-change', function (e, data) {
        if (value == true) {
            $('autoamount_%s').disabled='';
        } else {
            $('autoamount_%s').disabled='disabled';
        }
    });
    $('#autoamount_%s').on('switch-change', function (e, data) {
        if (value == true) {
            $('customamount_%s').disabled='';
        } else {
            $('customamount_%s').disabled='disabled';
        }
    });
</script>
""" % (person.name,person.id,person.d,person.id,person.id,person.id,person.id,person.id,person.id,person.id,person.id,person.id,person.id)
        customexpenseform.append(temp)
    
    return render(request, 'addexpense.html', {
        'form': form,
        'customexpenseform': customexpenseform
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
