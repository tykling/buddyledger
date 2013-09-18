import json
import sys
import decimal
from fractions import Fraction
from collections import defaultdict

def problem_from_buddy_format_to_foreign(pstruk):
    fin = {}
    
    fin["people"] = list(pstruk["userdict"].values())
    
    def old_to_new_user_id(userid):
        return fin["people"].index(pstruk["userdict"][userid])
    
    e = []
    for i in pstruk["expenselist"]:
        obj = {"whoshouldpay": [old_to_new_user_id(x) for x in i["users"]]}
        obj["whopaid"] = [{"amount": Fraction(payment["amount"]), "personId": old_to_new_user_id(payment["user"])} for payment in i["payments"]]
        e.append(obj)
    
    fin["expenses"] = e
    return fin

def conv_frac_to_decimal(f, precision):
    if f == 0: return decimal.Decimal("0")
    s = str(int(f)) + "."
    f -= int(f)
    with decimal.localcontext() as ctx:
        ctx.prec = precision
        s += str(decimal.Decimal(f.numerator) / f.denominator).partition(".")[2]
    return decimal.Decimal(s)

def result_from_foreign_format_to_buddy(result, olduserlist):
    #res = {olduserlist[k]: {olduserlist[i]: conv_frac_to_decimal(j, 2) for i,j in v.items() if j != 0} for k,v in result.items()}
    l = defaultdict(list)
    for k,v in result.items():
        for i,j in v.items():
            if i != j: l[olduserlist[i]].append((olduserlist[k], conv_frac_to_decimal(j, 2)))
    res = {i: dict(x) for i,x in l.items()}
    for i in olduserlist:
        if i not in res.keys():
            res[i] = {}
        if i not in res[i].keys():
            res[i][i] = "n/a"
    return res

if __name__ == "__main__":
    pythoncode = sys.stdin.read()
    pstruk = eval(pythoncode, globals(), {"Decimal": decimal.Decimal})
    convert_from_buddy_format(pstruk)
    print(json.dumps(fin))
