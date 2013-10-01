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
            self.fields['person_%s' % person.id] = forms.CheckboxInput(label=person.name)
            ### is the amount to be calculated or custom
            self.fields['person_%s_autoamount' % person.id] = forms.CheckboxInput(label="autoamount")
            ### field for specifying custom amount 
            self.fields['person_%s_customamount' % person.id] = forms.TextInput(label="amount")

    def get_expense_parts(self):
            for name, value in self.cleaned_data.items():
                if name.startswith('person_'):
                    yield (self.fields[name].label, value)

class PaymentForm(ModelForm):
    class Meta:
        model = Payment