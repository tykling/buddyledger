from django.forms import ModelForm, ValidationError
from buddyledger.models import Ledger
from buddyledger.models import Person
from buddyledger.models import Expense
from buddyledger.models import Payment


class LedgerForm(ModelForm):
    class Meta:
        model = Ledger


class PersonForm(ModelForm):
    class Meta:
        model = Person


class ExpenseForm(ModelForm):
    class Meta:
        model = Expense

    def __init__(self, *args, **kwargs):
        people = kwargs.pop('people')
        super(ExpenseForm, self).__init__(*args, **kwargs)

        for person in people:
            ### does this person have a part in this expense
            self.fields['person_expensepart_%s' % person.id] = forms.CheckboxInput(label=person.name,id=person.id)
            ### is the amount to be calculated or custom
            self.fields['person_autoamount_%s' % person.id] = forms.CheckboxInput(label="autoamount",id=person.id)
            ### field for specifying custom amount 
            self.fields['person_customamount_%s' % person.id] = forms.TextInput(label="amount",id=person.id)

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


class PaymentForm(ModelForm):
    class Meta:
        model = Payment