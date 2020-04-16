from decimal import *
from buddyledger.models import Ledger, Person, Expense, Currency
from django.shortcuts import render

def ConvertCurrency(amount,fromcurrencyid,tocurrencyid):
    if fromcurrencyid != tocurrencyid:
        fromcurrency = Currency.objects.get(pk=fromcurrencyid)
        tocurrency = Currency.objects.get(pk=tocurrencyid)    
        ### first convert to DKK
        dkkamount = Decimal(amount)*fromcurrency.dkk_price
        ### convert to tocurrency
        returnamount = dkkamount / tocurrency.dkk_price
        return Decimal(returnamount)
    else:
        ### same currency, just return the input
        return amount

def conv_frac_to_decimal(f, precision):
    if f == 0: return Decimal("0")
    s = str(int(f)) + "."
    f -= int(f)
    with localcontext() as ctx:
        ctx.prec = precision
        s += str(Decimal(f.numerator) / f.denominator).partition(".")[2]
    return Decimal(s)
    
def resultdict_to_decimal(resultdict):
    returndict = dict()
    for payerid, receiverdict in resultdict.items():
        for receiverid, amount in receiverdict.items():
            receiverdict[receiverid] = conv_frac_to_decimal(amount,2)
        returndict[payerid] = receiverdict
    return returndict

def render_to_response(request, templatename):
    return render(request, templatename, {}, content_type='text/html')
