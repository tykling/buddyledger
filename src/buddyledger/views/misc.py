from decimal import *
from buddyledger.models import Ledger, Person, Expense, Payment, Currency

def ConvertCurrency(amount,fromcurrencyid,tocurrencyid):
    fromcurrency = Currency.objects.get(pk=fromcurrencyid)
    tocurrency = Currency.objects.get(pk=tocurrencyid)
    ### first convert to DKK
    dkkamount = amount*fromcurrency.dkk_price
    ### convert to tocurrency
    returnamount = dkkamount / tocurrency.dkk_price
    return returnamount

def conv_frac_to_decimal(f, precision):
    if f == 0: return decimal.Decimal("0")
    s = str(int(f)) + "."
    f -= int(f)
    with decimal.localcontext() as ctx:
        ctx.prec = precision
        s += str(decimal.Decimal(f.numerator) / f.denominator).partition(".")[2]
    return decimal.Decimal(s)
    
def resultdict_to_decimal(resultdict):
    for payerid, receiverdict in resultdict.iteritems():
        for receiverid, amount in receiverdict:
            receiverdict[receiverid] = conv_frac_to_decimal(amount,2)
        returndict[payerid] = receiverdict
    return returndict
