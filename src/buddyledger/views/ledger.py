### datatypes
from collections import OrderedDict
from fractions import Fraction

### django functions
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect

### django models and forms
from buddyledger.models import Ledger, Person, Expense, ExpensePart, Currency
from buddyledger.forms import LedgerForm, PersonForm, ChangeMethodForm

### misc convenience functions
from buddyledger.views.misc import ConvertCurrency, resultdict_to_decimal

### calculation methods
from buddyledger.views.graphbuilder import solve_mincost_problem_for_expenses
from buddyledger.views.basiccalc import BasicCalc

### result layouts
from buddyledger.views.resultmatrix import ResultToMatrix

def CreateLedger(request):
    form = LedgerForm(request.POST or None)
    if form.is_valid(): # All validation rules pass
        ledger = Ledger(name=form['name'].data,currency_id=form['currency'].data)
        ledger.save()
        return HttpResponseRedirect('/ledger/%s' % ledger.id)

    return render(request, 'create_ledger.html', {
        'form': form,
    })


def ShowLedger(request, ledgerid=0):
    ### Check if the ledger exists - bail out if not
    try:
        ledger = Ledger.objects.get(pk = ledgerid)
    except Ledger.DoesNotExist:
        response = render_to_response('ledger_does_not_exist.html')
        return response
    
    ### get all people related to this ledger
    people = Person.objects.filter(ledger_id=ledgerid)

    ### get all expenses related to this ledger
    expenses = Expense.objects.filter(ledger_id=ledgerid)
    
    
    ### create dict with uid <> username mappings
    userdict = OrderedDict()
    userlist = []
    for person in people:
        userdict[person.id] = person.name  
        userlist.append(person.id)

    
    showresult = True
    errorlist = []
    calcdata = []
    if len(expenses) > 0:
        ### build the calcdata structure for calculation input
        for expense in expenses:            
            whopaid = []
            whoshouldpay = dict()
            
            ### loop through expenseparts (people) for this expense
            whopaid_total = 0
            shouldpay_total = 0
            inconsistent_expenses = []
            for expensepart in expense.expenseparts.filter(expense_id=expense.id):
                if expensepart.haspaid_native != 0:
                    whopaid.append(dict(personId=expensepart.person_id,amount=Fraction(expensepart.haspaid_native)))
                    whopaid_total += expensepart.haspaid_native
                if expensepart.shouldpay_native == None:
                    whoshouldpay[expensepart.person_id]=Fraction(0)
                else:
                    whoshouldpay[expensepart.person_id]=Fraction(expensepart.shouldpay_native)
                    shouldpay_total += expensepart.shouldpay_native
            
            ### check if this expense is consistent (neccesary because of an old bug)
            if shouldpay_total != expense.amount_native or whopaid_total != expense.amount_native:
                inconsistent_expenses.append(expense.id)
            
            ### add data for this expense to calcdata
            calcdata.append(dict(whopaid=whopaid, whoshouldpay=whoshouldpay))

        ### do the calculation
        if ledger.calcmethod == "optimized":
            fracresult = solve_mincost_problem_for_expenses(calcdata, userlist)
        elif ledger.calcmethod == "basic":
            fracresult = BasicCalc(calcdata,userlist)
        else:
            errorlist.append("Unknown calculation method selected for this ledger: <b>%s</b>. No result will be calculated.")
            showresult = False
    else:
        showresult = False
    
    ### do we have a result to show ?
    if showresult:
        ### convert the Fractions in the result to Decimal
        result = resultdict_to_decimal(fracresult)
    
        ### arrange the data for result output
        matrixdict = ResultToMatrix(result,userdict)

        ### render and return response
        return render(request, 'show_ledger.html', {
            'ledger': ledger,
            'people': people,
            'expenses': expenses,
            'debugdata': calcdata,
            'matrixdict': matrixdict,
            'userdict': userdict,
            'errorlist': errorlist,
            'inconsistent_expenses': inconsistent_expenses,
        })
    else:
        ### render and return response
        return render(request, 'show_ledger.html', {
            'ledger': ledger,
            'people': people,
            'expenses': expenses,
            'debugdata': calcdata,
            'userdict': userdict,
            'errorlist': errorlist,
        })


def EditLedger(request, ledgerid=0):
    ### Check if the ledger exists - bail out if not
    try:
        ledger = Ledger.objects.get(pk = ledgerid)
    except Ledger.DoesNotExist:
        response = render_to_response('ledger_does_not_exist.html')
        return response

    ### check if the ledger is open
    if ledger.closed:
        response = render_to_response('ledger_is_closed.html')
        return response
    
    if request.method == 'POST':
        form = LedgerForm(request.POST) # A form bound to the ledger data
        if form.is_valid(): # All validation rules pass
            ledger.name = form['name'].data
            ledger.currency_id = form['currency'].data
            ledger.save()
            return HttpResponseRedirect('/ledger/%s/#main' % ledger.id) # return to the ledger page
        else:
            form = LedgerForm(request.POST)
    else:
        form = LedgerForm(instance=ledger)

    return render(request, 'edit_ledger.html', {
        'form': form,
        'ledgerid': ledgerid
    })


def CloseLedger(request, ledgerid=0):
    ### Check if the ledger exists - bail out if not
    try:
        ledger = Ledger.objects.get(pk = ledgerid)
    except Ledger.DoesNotExist:
        response = render_to_response('ledger_does_not_exist.html')
        return response
    
    ### check if the ledger is open or closed
    if ledger.closed == True:
        response = render_to_response('ledger_not_open.html')
        return response

    if request.method == 'POST':
        ledger.closed = True
        ledger.save()
        return HttpResponseRedirect('/ledger/%s/#main' % ledger.id) # return to the ledger page
    else:
        return render(request, 'confirm_close_ledger.html', {
            'form': ConfirmCloseLedgerForm(),
            'expense': ledger
        })


def ReopenLedger(request, ledgerid=0):
    ### Check if the ledger exists - bail out if not
    try:
        ledger = Ledger.objects.get(pk = ledgerid)
    except Ledger.DoesNotExist:
        response = render_to_response('ledger_does_not_exist.html')
        return response
    
    ### check if the ledger is open or closed
    if ledger.closed == False:
        response = render_to_response('ledger_not_closed.html')
        return response

    if request.method == 'POST':
        ledger.closed = True
        ledger.save()
        return HttpResponseRedirect('/ledger/%s/#main' % ledger.id) # return to the ledger page
    else:
        return render(request, 'confirm_reopen_ledger.html', {
            'form': ConfirmReopenLedgerForm(),
            'expense': ledger
        })


def ChangeMethod(request, ledgerid=0):
    try:
        ledger = Ledger.objects.get(pk = ledgerid)
    except Ledger.DoesNotExist:
        response = render_to_response('ledger_does_not_exist.html')
        return response
    
    form = ChangeMethodForm(request.POST or None, initial={'calcmethod': ledger.calcmethod})
    if form.is_valid():
        ledger.calcmethod = form['calcmethod'].data
        ledger.save()
        return HttpResponseRedirect('/ledger/%s' % ledger.id)

    return render(request, 'change_ledger_method.html', {
        'form': form,
        'ledger': ledger,
    })

