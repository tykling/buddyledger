from django import forms
from buddyledger.models import Ledger, Person, Expense, Currency


class DeleteExpenseForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput())

class LedgerForm(forms.ModelForm):
    class Meta:
        model = Ledger


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person


class ExpenseForm(forms.Form):
    name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'id': 'name'}))
    amount = forms.CharField(max_length=10,widget=forms.TextInput(attrs={'id': 'amount', 'type': 'number'}))

    def __init__(self, *args, **kwargs):
        people = kwargs.pop('people')
        super(ExpenseForm, self).__init__(*args, **kwargs)
        
        ### add currency selectbox
        self.fields['currency'] = forms.ChoiceField(choices=((currency.id, currency.iso4217_code) for currency in Currency.objects.all()))
        
        ### add expensepart form elements
        for person in people:
            ### does this person have a part in this expense yes/no
            self.fields['person-expensepart-%s' % person.id] = forms.BooleanField(label=person.name,required=False)
            
            ### is the amount to be calculated or custom (relevant if yes above)
            self.fields['person-autoamount-%s' % person.id] = forms.BooleanField(label="autoamount",required=False)
            
            ### field for specifying custom amount (if custom amount above)
            self.fields['person-customamount-%s' % person.id] = forms.CharField(label="customamount", required=False)
            
            ### field for specifying payment amount
            self.fields['person-paymentamount-%s' % person.id] = forms.CharField(label="paymentamount", required=False)


    def get_expense_parts(self):
        fielddict = dict()
        for fieldname, value in self.cleaned_data.items():
            fielddict[fieldname] = value
        
        for fieldname,value in fielddict.iteritems():
            ### get the userid from the expensepart field
            if fieldname.startswith('person-expensepart-') and value == True:
                userid = fieldname[19:]
                
                ### find out if this user has a custom amount specified
                if 'person-autoamount-%s' % userid in fielddict and fielddict['person-autoamount-%s' % userid] == True:
                    ### calculate the amount for this user
                    shouldpay = "auto"
                else:
                    ### get the customamount for this user
                    shouldpay = fielddict['person-customamount-%s' % userid]
                
                ### find out if this user paid anything
                if 'person-paymentamount-%s' % userid in fielddict:
                    haspaid = fielddict['person-paymentamount-%s' % userid]
                else:
                    haspaid = 0
                
                ### return this user
                yield (userid, shouldpay, haspaid)
