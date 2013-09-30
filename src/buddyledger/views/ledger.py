### datatypes
from collections import OrderedDict
from fractions import Fraction

### django functions
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect

### django models and forms
from buddyledger.models import Ledger, Person, Expense, ExpensePart, Payment, Currency
from buddyledger.forms import LedgerForm, PersonForm, ExpenseForm, PaymentForm

### misc convenience functions
from buddyledger.views.misc import ConvertCurrency, resultdict_to_decimal

### calculation methods
from buddyledger.views.graphbuilder import solve_mincost_problem_for_expenses
from buddyledger.views.basiccalc import BasicCalc

### result layouts
from buddyledger.views.resultmatrix import ResultToMatrix

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
    
    ### put the input data structure for calculation together
    errorlist = []
    calcdata = []
    showresult = False
    for expense in expenses:
        expensepayments = Payment.objects.filter(expense_id = expense.id)
        ### no calculation if there are no payments
        if expensepayments != []:
            paymentlist = []
            totalamount = 0
            for payment in expensepayments:
                paymentlist.append(dict(personId=payment.person.id,amount=Fraction(payment.amount_native)))
                totalamount += payment.amount_native
            ### no calculation if the payments dont add up to the total expense
            if totalamount == expense.amount_native:
                showresult = True
                whoshouldpay = dict()
                for person in expense.people.all():
                    expensepart = ExpensePart.objects.get(expense=expense, person=person)
                    whoshouldpay[person.id]=expensepart.amount
                calcdata.append(dict(whopaid=paymentlist, whoshouldpay=whoshouldpay))
            elif totalamount < expense.amount_native:
                errorlist.append("The expense %s was not included in the calculation because the sum of the payments (%s) do not add up to the total expense (%s)" % (expense.name,totalamount,expense.amount_native))
            else:
                errorlist.append("The expense %s was not included in the calculation because the sum of the payments (%s) is larger than the total expense (%s)" % (expense.name,totalamount,expense.amount_native))
                
    ### create dict with uid <> username mappings
    userdict = OrderedDict()
    for person in people:
        userdict[person.id] = person.name

    ### do the calculation ? (true if at least one expense has payment(s) equal to the total expense)
    if showresult:
        if ledger.calcmethod == "optimized":
            fracresult = solve_mincost_problem_for_expenses(calcdata, [person.id for person in people])
        elif ledger.calcmethod == "basic":
            fracresult = BasicCalc(calcdata,[person.id for person in people])
        else:
            errorlist.append("Unknown calculation method selected for this ledger: <b>%s</b>. No result will be calculated.")
            showresult = False
        
    if showresult:
        ### convert the Fractions in the result to Decimal
        result = resultdict_to_decimal(fracresult)
    
        ### arrange the data for result output
        matrixdict = ResultToMatrix(result,userdict)
        #tabledict = ResultToTable(result,userdict)
        tabledict = dict() #not implemented yet

        ### render and return response
        return render(request, 'showledger.html', {
            'ledger': ledger,
            'people': people,
            'expenses': expenses,
            'payments': payments,
            'debugdata': calcdata,
            'matrixdict': matrixdict,
            'tabledict': tabledict,
            'userdict': userdict,
            'errorlist': errorlist
        })
    else:
        ### render and return response
        return render(request, 'showledger.html', {
            'ledger': ledger,
            'people': people,
            'expenses': expenses,
            'payments': payments,
            'debugdata': calcdata,
            'errorlist': errorlist
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

