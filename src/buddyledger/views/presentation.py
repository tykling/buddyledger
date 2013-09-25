from collections import OrderedDict
from decimal import *

def ResultToMatrix(result,userdict):
    ### build all zero matrix table (dict of dicts)
    table = OrderedDict()
    resultdict = OrderedDict()

    ### first create the top <th> row with all the names
    temp = OrderedDict()
    temp[0] = "n/a" # the 0,0 field is the upper left position
    counter=0

    for user in userdict:
        counter += 1
        temp[counter] = "%s pay" % user
    resultdict[0] = temp
    
    ### now create a row per user
    rowcounter=0
    for user in userdict:
        rowcounter += 1
        ### create new empty table row
        temp = OrderedDict()
        ### the leftmost column with the name
        temp[0] = "%s receive" % user
        
        ### loop through users, add Decimal(0) or "n/a"
        colcounter=0
        for tempuser in userdict:
            colcounter += 1
            if user == tempuser:
                temp[colcounter] = "n/a"
            else:
                temp[colcounter] = Decimal(0)
        
        ### add this row to the table
        resultdict[rowcounter] = temp

    ### now loop through the result and insert the debts into the matrix,
    ### and calculate totals while we are here
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
    counter=0
    for number,row in resultdict.iteritems():
        ### the position of the rightmost column, plus one
        pos = len(row)+1

        if counter == 0:
            ### this is the first row, just add <th> for the rightmost totals column
            row[pos] = "Total Receive"
        else:
            ### add the rightmost "total receive" column for this row
            row[pos] = receivertotal[counter-1]
        counter += 1

    ### create the new bottom row for the "total pay" amounts
    temp = OrderedDict()
    temp[0] = "Total Pay"
    for number,amount in payertotal.iteritems():
        temp[number+1] = amount

    return resultdict

def ResultToTable(result,userdict):
    # not implemented yet
    return OrderedDict()
