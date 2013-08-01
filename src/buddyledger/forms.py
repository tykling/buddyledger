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

    ### custom validation function for the amount field,
    ### since amount is a bigint field the default validation rules do not allow decimals,
    ### just check that amount is numeric and send it on
    def clean_amount(self):
        data = self.cleaned_data.get('amount')
        try:
            float(data)
            return data
        except ValueError:
            raise forms.ValidationError("invalid amount")


class PaymentForm(ModelForm):
    class Meta:
        model = Payment

    ### custom validation function for the amount field,
    ### since amount is a bigint field the default validation rules do not allow decimals,
    ### just check that amount is numeric and send it on
    def clean_amount(self):
        data = self.cleaned_data.get('amount')
        try:
            float(data)
            return data
        except ValueError:
            raise forms.ValidationError("invalid amount")