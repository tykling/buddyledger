def BasicCalc(expenses, peoplelist):
    debtdict = dict()
    ### loop through expenses
    for expense in expenses:
        ### loop through each payment in this expense
        for payerdict in expense['whopaid']:
            ### count the number of people splitting this expense
            splitters = 0
            for splituserid in expense['whoshouldpay']:
                if expense['whoshouldpay'][splituserid] == 0:
                    # this user should not pay any part of this expense
                    continue
                splitters += 1

            # nobody wants to pay? not supposed to happen
            if not splitters:
                return False

            ### find out if the payer is paying part of this expense, if so, substract payers own part of the payment
            if payerdict['personId'] in expense['whoshouldpay']:
                finalamount = payerdict['amount'] - payerdict['personId']

            ### loop through the users splitting this expense,
            ### and add their part of this expense to their debt to the payer
            for splituserid in expense['whoshouldpay']:
                if expense['whoshouldpay'][splituserid] == 0:
                    # this user should not pay any part of this expense
                    continue

                ### initialize this userids slot in the debtdict
                if not splituserid in debtdict:
                    debtdict[splituserid] = dict()

                ### add this splitusers part of the payment to his debt to the payer
                ### unless the splituser is also the payer (no need to pay to oneself)
                if payerdict['personId'] == splituserid:
                    continue

                # initialize dict
                if payerdict['personId'] not in debtdict[splituserid]:
                    debtdict[splituserid][payerdict['personId']] = 0

                # add this users part of this payment to the users debt to the payer
                debtdict[splituserid][payerdict['personId']] += finalamount/splitters

    ### optimize payments to the same people dont have to pay to eachother,
    for payerid in list(debtdict):
        receiverdict = debtdict[payerid]
        for receiverid,amount in receiverdict.iteritems():
            ### make certain everything is initialized
            if not payerid in debtdict:
                debtdict[payerid] = dict()
            if not receiverid in debtdict[payerid]:
                debtdict[payerid][receiverid] = 0
            if not receiverid in debtdict:
                debtdict[receiverid] = dict()
            if not payerid in debtdict[receiverid]:
                debtdict[receiverid][payerid] = 0

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
