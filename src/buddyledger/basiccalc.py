def BasicCalc(expenses, numPeople):
    ### loop through expenses
    for expense in expenses.iteritems():
        ### loop through each payment in this expense
        for payerdict in expense['whopaid']:
            ### loop through the users splitting this expense,
            ### and add their part of this expense to their debt to the payer
            for splituser in expense['whoshouldpay']:
                ### add this splitusers part of the payment to his debt to the payer
                ### unless the splituser is also the payer
                if payerdict['personId'] != splituser:
                    debtdict[splituser][payerdict['personId']] += payerdict['amount']/expense['whoshouldpay']

    ### optimize payments to the same people dont have to pay to eachother
    for payerid,receiverdict in debtdict.iteritems():
        for receiverid,amount in receiverdict:
            ### if receiver and payer is the same person, skip this row
            if payerid == receiverid:
                continue
            
            ### if either one is 0 skip it
            if debtdict[payerid][receiverid] == 0 or debtdict[receiverid][payerid] == 0:
                continue

            ### check if receiver is to receive more than he is paying to this payer
            if debtdict[receiverid][payerid] > debtdict[payerid][receiverid]:
                #print "%s > %s - optimizing %s away..." % (debtdict[receiverid][payerid],debtdict[payerid][receiverid],debtdict[payerid][receiverid])
                debtdict[receiverid][payerid] = debtdict[receiverid][payerid] - debtdict[payerid][receiverid]
                debtdict[payerid][receiverid] = 0
            elif debtdict[receiverid][payerid] < debtdict[payerid][receiverid]:
                #print "%s < %s - optimizing %s away..." % (debtdict[receiverid][payerid],debtdict[payerid][receiverid],debtdict[receiverid][payerid])
                debtdict[payerid][receiverid] = debtdict[payerid][receiverid] - debtdict[receiverid][payerid]
                debtdict[receiverid][payerid] = 0
            else:
                #print "%s == %s - optimizing both away" % (debtdict[receiverid][payerid],debtdict[payerid][receiverid])
                if debtdict[payerid][receiverid] != 0:
                    debtdict[payerid][receiverid] = 0
                    debtdict[receiverid][payerid] = 0
    
    ### return the result
    return debtdict
