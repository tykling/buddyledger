#!/usr/bin/python
import random
#from tarjan import tarjan

class MonoPayment:
    def __init__(self,receiver,payer,amount):
        self.receiver = receiver
        self.payer    = payer
        self.amount   = amount

class PaymentProcessor:
    def create_monopayments(self,paymentdictlist): 
        ### create (mono)payments list from payments list
        self.monopayments = []
        for payment in paymentdictlist:
            totalamount = float(0)
            payerweight = []
            for payer in payment['payments']:
                totalamount += float(payer['amount'])
            for payer in payment['payments']:
                payerweight.append(float(payer['amount'])/totalamount)
            self.graphpayment = {}
            for user in payment['users']:
                for (n,payer) in list(enumerate(payment['payments'])):
                    self.graphpayment[user] = [] 
                    self.graphpayment[payer['user']] = []
                    if user != payer['user']:
                        amount      = totalamount * (1/float(len(payment['users']))) * payerweight[n] 
                        monopayment = MonoPayment(user,payer['user'],amount)
                        self.monopayments.append(monopayment)

    def abs2neg_payments(self):
        #standardize payments
        for (n,payment) in list(enumerate(self.monopayments)):
            if payment.receiver < payment.payer:
                self.monopayments[n] = MonoPayment(receiver=payment.payer,payer=payment.receiver, amount = -1 * payment.amount)

    def sum_eq_payments(self,static=0):
        payment = self.monopayments[static]
        for (n,otherpayment) in list(enumerate(self.monopayments)):
            if n != static:
                #print 'otherpayment.receiver: %s  otherpayment.payer: %s' % (otherpayment.receiver,otherpayment.payer)
                #print 'payment.receiver: %s  payment.payer: %s' % (payment.receiver,payment.payer)
                if otherpayment.receiver == payment.receiver and otherpayment.payer == payment.payer:
                    self.monopayments[static].amount += otherpayment.amount
                    self.monopayments[n] = False
                elif otherpayment.receiver == payment.payer and otherpayment.payer == payment.receiver:
                    self.monopayments[static].amount -= otherpayment.amount
                    self.monopayments[n] = False
        for (n,paym) in reversed(list(enumerate(self.monopayments))):
            if not paym:
                self.monopayments.remove(paym)

    def neg2abs_payments(self):
        for (n,payment) in list(enumerate(self.monopayments)):
            if payment.amount < 0:
                self.monopayments[n] = MonoPayment(receiver=payment.payer,payer=payment.receiver, amount = -1 * payment.amount)
    ## THIS CRAP WILL BE REMOVED
    def reduce_monopayments(self,pay1idx=0):
        payment1 = self.monopayments[pay1idx]
        done = False
        for (n,payment2) in list(enumerate(self.monopayments)): 
            if payment1.receiver == payment2.payer:
                for (k,payment3) in list(enumerate(self.monopayments)):
                    if k != n and payment2.payer == payment1.payer:
                        self.monopayments[k].amount += self.monopayments[n].amount
                        self.monopayments[n] = False
        for m in reversed(range(len(self.monopayments))):
           if not self.monopayments[m]:
                self.monopayments.pop(m) 

    def walkthrough_idxs(self,fcn):
        fcns = { 'reduce_monopayments' : self.reduce_monopayments,
                 'sum_eq_payments'     : self.sum_eq_payments }
        keepgoing = True
        while True:
            for n in reversed(range(len(self.monopayments))):
                fcns[fcn](n)
                if n > len(self.monopayments) - 1:
                    break
                succesful_parsing = True
                if succesful_parsing:
                    keepgoing = False
            if not keepgoing:
                break

    def monopayments2graph(self):
        for payment in self.monopayments:
            self.graphpayment[payment.payer].append(payment.receiver)
    
    def findmonopayment(self,payer,receiver,returnidx=False):
        for (n,payment) in list(enumerate(self.monopayments)):
            if payment.receiver == receiver and payment.payer == payer:
                if returnidx:
                    return n
                else:
                    return payment
        return False

    def removegraphcycles(self):
        cycles = tarjan(self.graphpayment)
        print cycles
        for cycle in cycles:
            if len(cycle)>1:
                if len(cycle) == 2:
                    A = findmonopayment(cycle[0],cycle[1])
                    Aidx = findmonopayment(cycle[0],cycle[1],returnidx=True)
                    B = findmonopayment(cycle[1],cycle[0])
                    B.amount -= A.amount
                    self.monopayments.pop(Aidx)
                elif len(cycle) == 3:
                    if one2two:
                        print 'stuff to be done'
                    else:
                        print 'stuff to be done'
                elif len(cycle) > 3:
                        print 'stuff to be done'
                else:
                    print 'THIS SHOULD NOT HAPPEN'
                #for receiver in cycle[1:]:
            
    def __init__(self,paymentdictlist,method='b2'):
        ## Creates self.monopayments which is the output to use
        self.method = method 
        if method == 'b2':
            self.create_monopayments(paymentdictlist)
            self.abs2neg_payments()
            #self.monopayments2graph()
            #self.removegraphcycles()
            self.walkthrough_idxs('sum_eq_payments')
            self.neg2abs_payments()
            #self.walkthrough_idxs('reduce_monopayments') will be fixed soon
