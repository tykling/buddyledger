from collections import OrderedDict
from decimal import *


def ResultToMatrix(result,userdict):
    ### first get an empty matrix (dict of dicts)
    resultdict = GetEmptyMatrix(userdict)

    ### now populate the matrix with the results
    resultdict = PopulateMatrix(result,resultdict,userdict)

    ### return the finished matrix
    return resultdict


def GetEmptyMatrix(userdict):
    ### build all zero matrix table (dict of dicts)
    table = OrderedDict()
    resultdict = OrderedDict()

    ### first create the top <th> row with all the names
    temp = OrderedDict()
    temp[0] = "n/a" # the 0,0 field is the upper left position

    for userid,username in userdict.items():
        temp[userid] = "%s pay" % username
    resultdict[0] = temp
    
    ### now create a row per user
    for receiverid,receivername in userdict.items():
        ### create new empty table row
        temp = OrderedDict()
        ### add the rows leftmost column with the name
        temp[0] = "%s receive" % receivername
        
        ### loop through users, add Decimal(0) or "n/a"
        for payerid,payername in userdict.items():
            if receivername == payername:
                temp[payerid] = "n/a"
            else:
                temp[payerid] = Decimal(0)
        
        ### add this row to the table
        resultdict[receiverid] = temp    
    return resultdict


def PopulateMatrix(result,resultdict,userdict):
    ### loop through the result and insert the debts into the matrix,
    ### and also calculate the totals while we are here
    payertotal = OrderedDict()
    receivertotal = OrderedDict()
    for userid,username in userdict.items():
        payertotal[userid] = 0
        receivertotal[userid] = 0

    for payerid, receiverdict in result.items():
        for receiverid, amount in receiverdict.items():
            ### add to totals for this payer
            payertotal[payerid] += amount

            ### add to totals for this receiver
            receivertotal[receiverid]+=amount

            ### add to resultdict
            resultdict[receiverid][payerid] = amount


    ### add totals columns and row to the matrix (bottom row and rightmost column)
    for receiverid,row in resultdict.items():
        
        ### add the rightmost column for this row
        if receiverid == 0:
            ### this is the first row, just add <th> for the rightmost totals column
            resultdict[0]['total'] = "Total Receive"
        else:
            ### add the rightmost "total receive" column for this row
            resultdict[receiverid]['total'] = receivertotal[receiverid]

    ### create the new bottom row for the "total pay" amounts and add it to resultdict
    temp = OrderedDict()
    temp[0] = "Total Pay"
    for userid,username in userdict.items():
        amount = payertotal[userid]
        temp[userid] = amount
    temp['total'] = 'n/a'
    resultdict['total'] = temp


    ### return the populated matrix
    return resultdict

