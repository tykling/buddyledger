def ResultToMatrix(result,userdict,personcounterdict):
    ### build all zero matrix table (dict of dicts)
    table = OrderedDict()
    
    ### first create the top <th> row with all the names
    temp = OrderedDict()
    temp[0] = "n/a" # the 0,0 field is the upper left position
    counter=0
    for user in userdict:
        counter++
        temp[counter] = "%s pay" % user
    resultdict[0] = temp
    
    ### now create a row per user
    rowcounter=0
    for user in userdict:
        rowcounter++
        ### create new empty table row
        temp = OrderedDict()
        ### the leftmost column with the name
        temp[0] = "%s receive" % user
        
        ### loop through users, add Decimal(0) or "n/a"
        colcounter=0
        for tempuser in userdict:
            colcounter++
            if user == tempuser:
                temp[colcounter] = "n/a"
            else:
                temp[colcounter] = Decimal(0)
        
        ### add this row to the table
        resultdict[rowcounter] = temp

        ### now loop through the result and insert the debts into the matrix,
        ### and calculate totals while we are here
        payertotal = dict()
        receivertotal = dict()
        for payerid, receiverdict in result.iteritems():
            ### find the counter number of this payerid
            payernumber = personcounterdict[payerid]
            for receiverid, amount in receiverdictiteritems():
                ### add to totals for this payer
                payertotal[payernumber]+=amount
                receivernumber = personcounterdict[receiverid]
                ### add to totals for this receiver
                receivertotal[receivernumber]+=amount
                resultdict[receivernumber][payernumber] = amount
                    
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
        counter++

    ### create the new bottom row for the "total pay" amounts
    temp = OrderedDict()
    temp[0] = "Total Paý"
    for number,amount in payertotal.iteritems():
        temp[number+1] = amount

    return resultdict

def ResultToTable(result,userdict,personcounterdict):
    # not implemented yet
    return dict()
