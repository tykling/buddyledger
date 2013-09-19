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
