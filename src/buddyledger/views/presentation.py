from collections import OrderedDict
from decimal import *


def ResultToMatrix(result,userdict):
    ### first get an empty matrix (dict of dicts)
    resultdict = GetEmptyMatrix(userdict)

    ### now populate the matrix with the results
    resultdict = PopulateMatrix(result,resultdict)

    ### return the finished matrix
    return resultdict


def GetEmptyMatrix(userdict):
    ### build all zero matrix table (dict of dicts)
    table = OrderedDict()
    resultdict = OrderedDict()

    ### first create the top <th> row with all the names
    temp = OrderedDict()
    temp[0] = "n/a" # the 0,0 field is the upper left position

    for userid,username in userdict.iteritems():
        temp[userid] = "%s pay" % username
    resultdict[0] = temp
    
    ### now create a row per user
    for receiverid,receivername in userdict.iteritems():
        ### create new empty table row
        temp = OrderedDict()
        ### add the rows leftmost column with the name
        temp[0] = "%s receive" % receivername
        
        ### loop through users, add Decimal(0) or "n/a"
        for payerid,payername in userdict.iteritems():
            if receivername == payername:
                temp[payerid] = "n/a"
            else:
                temp[payerid] = Decimal(0)
        
        ### add this row to the table
        resultdict[receiverid] = temp    
    return resultdict


def PopulateMatrix(result,resultdict):
    ### loop through the result and insert the debts into the matrix,
    ### and also calculate the totals while we are here
    payertotal = OrderedDict()
    receivertotal = OrderedDict()
    for payerid, receiverdict in result.iteritems():
        for receiverid, amount in receiverdict.iteritems():
            ### add to totals for this payer
            if payerid in payertotal:
                payertotal[payerid] += amount
            else:
                payertotal[payerid] = amount

            ### add to totals for this receiver
            if receiverid in receivertotal:
                receivertotal[receiverid]+=amount
            else:
                receivertotal[receiverid]=amount
            resultdict[receiverid][payerid] = amount


    ### add totals columns and row to the matrix (bottom row and rightmost column)
    for receiverid,row in resultdict.iteritems():
        
        ### add the rightmost column for this row
        if receiverid == 0:
            ### this is the first row, just add <th> for the rightmost totals column
            resultdict[0]['total'] = "Total Receive"
        else:
            ### add the rightmost "total receive" column for this row
            resultdict[receiverid]['total'] = receivertotal[receiverid]

    ### create the new bottom row for the "total pay" amounts
    temp = OrderedDict()
    temp[0] = "Total Pay"
    for payerid,amount in payertotal.iteritems():
        temp[payerid] = amount
    
    ### return the populated matrix
    return resultdict


def ResultToTable(result,userdict):
    # not implemented yet
    return OrderedDict()
