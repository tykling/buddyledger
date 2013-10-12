from django import forms
from buddyledger.models import Ledger, Person, Expense, Currency


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
            self.fields['person_expensepart_%s' % person.id] = forms.BooleanField(label=person.name,required=False)
            
            ### is the amount to be calculated or custom (relevant if yes above)
            self.fields['person_autoamount_%s' % person.id] = forms.BooleanField(label="autoamount",required=False)
            
            ### field for specifying custom amount (if custom amount above)
            self.fields['person_customamount_%s' % person.id] = forms.CharField(label="customamount", required=False)


    def get_expense_parts(self):
        for fieldname, value in self.cleaned_data.items():
            ### get the userid from the expensepart field
            if fieldname.startswith('person_expensepart_'):
                userid = fieldname[19:]
                
                ### find out if this user has a custom amount specified
                if 'person_autoamount_%s' % userid in self.fields:
                    ### calculate the amount for this user
                    shouldpay = "auto"
                else:
                    ### get the customamount for this user
                    shouldpay = self.fields['person_customamount_%s' % userid].value
                
                ### find out how much the user has paid
                haspaid = self.fields['person_paymentamount_%s' % userid].value
                
                ### return this user
                yield (userid, shouldpay, haspaid)
