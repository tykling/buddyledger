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


class PaymentForm(ModelForm):
    class Meta:
        model = Payment