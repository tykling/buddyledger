from django import forms
from buddyledger.models import Ledger, Person, Expense, Payment, Currency


class LedgerForm(forms.ModelForm):
    class Meta:
        model = Ledger


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person


class ExpenseForm(forms.Form):
    name = forms.CharField(max_length=30)
    amount = forms.CharField(max_length=10)

    def __init__(self, *args, **kwargs):
        people = kwargs.pop('people')
        super(ExpenseForm, self).__init__(*args, **kwargs)
        
        ### add currency selectbox
        self.fields['currency'] = forms.ChoiceField(choices=((currency.id, currency.name) for currency in Currency.objects.all()))
        
        ### add expensepart form elements
        for person in people:
            ### does this person have a part in this expense
            self.fields['person_expensepart_%s' % person.id] = forms.BooleanField(label=person.name,required=False, widget=forms.CheckboxInput(attrs={'id': person.id}))
            ### is the amount to be calculated or custom
            self.fields['person_autoamount_%s' % person.id] = forms.BooleanField(label="autoamount",required=False, widget=forms.CheckboxInput(attrs={'id': person.id}))
            ### field for specifying custom amount 
            self.fields['person_customamount_%s' % person.id] = forms.CharField(label="customamount", required=False, widget=forms.TextInput(attrs={'id': person.id}))
        

    def get_expense_parts(self):
        for fieldname, value in self.cleaned_data.items():
            ### if this is a customamount textfield
            if fieldname.startswith('person_customamount_'):
                ### and the person is part of this expense
                if 'person_expensepart_%s' % self.fields[fieldname].id in self.cleaned_data:
                    ### return userid and amount
                    yield (self.fields[fieldname].id, value)
            ### if this is an autoamount checkbox
            if fieldname.startswith('person_autoamount_'):
                ### and the person is part of this expense
                if 'person_expensepart_%s' % self.fields[fieldname].id in self.cleaned_data:
                    ### return userid and None for amount
                    yield (self.fields[fieldname].id, None)


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment