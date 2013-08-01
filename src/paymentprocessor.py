#!/usr/bin/python
import random

class MonoPayment:
    def __init__(self,receiver,payer,amount):
        self.receiver = receiver
        self.payer    = payer
        self.amount   = amount

class PaymentProcessor:
#18:57 < Tykling> borgtu: [{'amount': 100, 'payments': [{'amount': 100, 'user': 1}], 'users': [1, 2, 3]}, {'amount': 1000, 'payments': [{'amount': 100, 'user': 2}, 
#                 {'amount': 900, 'user': 1}], 'users': [2, 3]}]
#18:58 < Tykling> {'amount': 100, 'payments': [{'amount': 100, 'user': 1}], 'users': [1, 2, 3]}
#18:58 < Tykling> {'amount': 1000, 'payments': [{'amount': 100, 'user': 2}], 'users': [2, 3]}

    def create_monopayments(self,paymentdictlist): 
        ### create (mono)payments list from payments list
        self.monopayments = []
        for payment in paymentdictlist:
            for receiver in payment['receiver']:
                for payer in payment['payer']:
                    self.monopayments.append(MonoPayment(receiver,payer,payment['amount']/(len(payment['receiver'])+len(payment['payer']))))    

    def abs2neg_payments(self):
        #standardize payments
        for (n,payment) in list(enumerate(self.monopayments)):
            if payment.receiver < payment.payer:#NO IDEA WHAT THE ORDERING IS ATM
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
                    print 'lol'
                elif otherpayment.receiver == payment.payer and otherpayment.payer == payment.receiver:
                    self.monopayments[static].amount -= otherpayment.amount
                    self.monopayments[n] = False
                    print 'lol2'
        for (n,paym) in reversed(list(enumerate(self.monopayments))):
            if not paym:
                self.monopayments.remove(paym)

    def neg2abs_payments(self):
        for (n,payment) in list(enumerate(self.monopayments)):
            if payment.amount < 0:
                self.monopayments[n] = MonoPayment(receiver=payment.payer,payer=payment.receiver, amount = -1 * payment.amount)
    ## THIS WILL BE REMOVED
    def reduce_monopayments(self,pay1idx=0):
        payment1 = self.monopayments[pay1idx] #B owes A
        done = False
        for (n,payment2) in list(enumerate(self.monopayments)): #payment = B
            if payment1.receiver == payment2.payer:
                # payment2 = A ows C is found
                for (k,payment3) in list(enumerate(self.monopayments)):
                    # payment3 B owes C
                    #n is 2, k is 3
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

    def __init__(self,paymentdictlist,method='b2'):
        ## Creates self.monopayments which is the output to use
        self.method = method 
        if method == 'b2':
            self.create_monopayments(paymentdictlist)
            self.abs2neg_payments()
            self.walkthrough_idxs('sum_eq_payments')
            self.neg2abs_payments()
            #self.walkthrough_idxs('reduce_monopayments')

