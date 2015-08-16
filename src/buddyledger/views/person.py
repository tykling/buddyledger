from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages

from buddyledger.forms import PersonForm, DeletePersonForm
from buddyledger.models import Ledger, Person, Expense, Currency

def AddPerson(request,ledgerid=0):
    ### check if the ledger exists, bail out if not
    try:
        ledger = Ledger.objects.get(pk = ledgerid)
    except Ledger.DoesNotExist:
        response = render_to_response('ledgerdoesnotexist.html')
        return response

    ### check if the ledger is open
    if ledger.closed:
        response = render_to_response('ledger_is_closed.html')
        return response

    if request.method == 'POST':
        form = PersonForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            person = Person(ledger_id=ledgerid,name=form['name'].data)
            person.save() # save the new person
            return HttpResponseRedirect('/ledger/%s/#people' % ledgerid) # return to the ledger page
        else:
            form = PersonForm(request.POST)
    else:
        form = PersonForm()

    return render(request, 'add_person.html', {
        'form': form,
    })


def EditPerson(request, personid=0):
    ### Check if the person exists - bail out if not
    try:
        person = Person.objects.get(pk = personid)
    except Person.DoesNotExist:
        response = render_to_response('person_does_not_exist.html')
        return response

    
    ### check if the ledger is open
    ledger = Ledger.objects.get(pk=person.ledger.id)
    if ledger.closed:
        response = render_to_response('ledger_is_closed.html')
        return response

    if request.method == 'POST':
        form = PersonForm(request.POST) # A form bound to the person data
        if form.is_valid(): # All validation rules pass
            person.name = form['name'].data
            person.save()
            return HttpResponseRedirect('/ledger/%s/#people' % person.ledger.id) # return to the ledger page
        else:
            form = PersonForm(request.POST)
    else:
        form = PersonForm(instance=person)

    return render(request, 'edit_person.html', {
        'form': form,
        'person': person
    })


def RemovePerson(request, personid=0):
    ### Check if the person exists - bail out if not
    person = get_object_or_404(Person, id=personid)

    ### check if the ledger is open
    if person.ledger.closed:
        response = render_to_response('ledger_is_closed.html')
        return response

    expenses = person.expense_set.all()
    if expenses:
        return render_to_response('expense_references_this_person.html', {
            'expenses': expenses, 
            'ledger_id': person.ledger.id, 
            'person': person
        })

    ### confirm delete
    form = DeletePersonForm(request.POST or None, instance=person)
    if form.is_valid():
        person.delete()
        messages.success(request, 'The person "%s" has been deleted.' % person.name)
        return HttpResponseRedirect('/ledger/%s/#people' % person.ledger.id) # return to the list of people

    return render(request, 'confirm_person_delete.html', {
        'person': person,
        'form': form
    })

