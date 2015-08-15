from django import forms
from buddyledger.models import Ledger, Person, Expense, Currency, ExpensePart
import datetime

### confirmation forms
class DeleteExpenseForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput())


class ConfirmCloseLedgerForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput())


class ConfirmReopenLedgerForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput())


### ModelForms
class LedgerForm(forms.ModelForm):
    class Meta:
        model = Ledger
        fields = '__all__'


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'


### custom forms
class ExpenseForm(forms.Form):
    name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'id': 'name'}))
    amount = forms.DecimalField(min_value=0, decimal_places=2, widget=forms.NumberInput(attrs={'id': 'amount'}))
    date = forms.DateField()

    def __init__(self, *args, **kwargs):
        people = kwargs.pop('people')
        if 'expenseparts' in kwargs:
            expenseparts = kwargs.pop('expenseparts')
        else:
            expenseparts = False
        super(ExpenseForm, self).__init__(*args, **kwargs)
        
        ### add currency selectbox
        self.fields['currency'] = forms.ChoiceField(choices=((currency.id, currency.iso4217_code) for currency in Currency.objects.all()))
        
        ### add expensepart form elements
        if expenseparts:
            ### this is an edit expense form
            for person in people:
                try:
                    ep = expenseparts.get(person=person)
                except ExpensePart.DoesNotExist:
                    ep = False

                if ep:
                    ### this person has a part in this expense
                    self.fields['person-expensepart-%s' % person.id] = forms.BooleanField(label=person.name, required=False, initial=True)
                    
                    ### is the amount to be calculated or custom (relevant only if yes above)
                    self.fields['person-autoamount-%s' % person.id] = forms.BooleanField(label="autoamount", required=False, initial=ep.autoamount)
                        
                    ### field for specifying custom amount (relevant only if custom amount above)
                    self.fields['person-customamount-%s' % person.id] = forms.DecimalField(label="customamount", required=False, initial=ep.shouldpay, min_value=0, decimal_places=2)
                    
                    ### field for specifying payment amount
                    self.fields['person-paymentamount-%s' % person.id] = forms.DecimalField(label="paymentamount", required=False, initial=ep.haspaid, min_value=0, decimal_places=2)
                else:
                    ### this person does NOT have a part in this expense
                    self.fields['person-expensepart-%s' % person.id] = forms.BooleanField(label=person.name, required=False, initial=False)
                    
                    ### is the amount to be calculated or custom (relevant only if yes above)
                    self.fields['person-autoamount-%s' % person.id] = forms.BooleanField(label="autoamount", required=False)
                    
                    ### field for specifying custom amount (relevant only if custom amount above)
                    self.fields['person-customamount-%s' % person.id] = forms.DecimalField(label="customamount", required=False, min_value=0, decimal_places=2)
                    
                    ### field for specifying payment amount
                    self.fields['person-paymentamount-%s' % person.id] = forms.DecimalField(label="paymentamount", required=False, min_value=0, decimal_places=2)
        else:
            for person in people:
                ### does this person have a part in this expense yes/no
                self.fields['person-expensepart-%s' % person.id] = forms.BooleanField(label=person.name, required=False)
                
                ### is the amount to be calculated or custom (relevant only if yes above)
                self.fields['person-autoamount-%s' % person.id] = forms.BooleanField(label="autoamount", required=False)
                
                ### field for specifying custom amount (relevant only if custom amount above)
                self.fields['person-customamount-%s' % person.id] = forms.DecimalField(label="customamount", required=False, min_value=0, decimal_places=2)
                
                ### field for specifying payment amount
                self.fields['person-paymentamount-%s' % person.id] = forms.DecimalField(label="paymentamount", required=False, min_value=0, decimal_places=2)


    def get_expense_parts(self):
        fielddict = dict()
        for fieldname, value in self.cleaned_data.items():
            fielddict[fieldname] = value
        
        expenseparts = dict()
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

                ### add this user to expenseparts
                if haspaid == '' or not haspaid:
                    haspaid = 0
                if shouldpay == '' or not shouldpay:
                    shouldpay = 0
                expenseparts[userid] = dict(shouldpay=shouldpay, haspaid=haspaid)
        return expenseparts


CALCMETHODS = (
    ('basic', 'basic'),
    ('optimized', 'optimized'),
)
    
class ChangeMethodForm(forms.Form):
    calcmethod = forms.ChoiceField(choices=CALCMETHODS)

