import random
from tarjan import tarjan

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

    def findmonopayment(self,payer,receiver):
        for (n,payment) in list(enumerate(self.monopayments)):
            if payment.receiver == receiver and payment.payer == payer:
                return n
        return False

    def cycle2monopaymentlist(self,cycle):
        listidx = []
        for n in range(len(cycle)-1):
           listidx.append(findmonopayment(cycle[n],cycle[n+1],True))
        return listidx
    
    ### This returns false every time since tarjans algorithm does not detect these since they are not strongly connected
    def verify_one2two(self,payidxs):
        for n in range(len(payidxs)):
            if (self.monopayments[n].receiver == self.monopayments[(n+1)%3].receiver) or (self.monopayments[n].payer == self.monopayments[(n+1)%3].payer):
                return False
        return False

   
    def removedigraphcycles(self):
        cycles = tarjan(self.graphpayment)
        for cycle in cycles:
            if len(cycle)>1:
                if len(cycle) == 2:
                    Aidx = self.findmonopayment(cycle[0],cycle[1])
                    Bidx = self.findmonopayment(cycle[1],cycle[0])
                    self.monopayments[Bidx].amount -= self.monopayments[Aidx].amount
                    self.monopayments.pop(self.monopayments[Aidx])
                elif len(cycle) > 2:
                    paymentidxs = cycle2monopaymentlistidx(cycle)
                    for n in range(1,len(paymentidxs)):
                        self.monopayments[paymentidxs[n]].amount -= self.monopayments[paymentidxs[0]]
                    self.monopayments.pop[paymentidxs[0]]
                else:
                    print 'THIS SHOULD NOT HAPPEN'
            
    def __init__(self,paymentdictlist,method='b2'):
        ## Creates self.monopayments which is the output to use
        self.method = method 
        if method == 'b2':
            self.create_monopayments(paymentdictlist)
            self.abs2neg_payments()
            self.walkthrough_idxs('sum_eq_payments')
            self.monopayments2graph()
            self.removedigraphcycles()
            self.walkthrough_idxs('sum_eq_payments')
            self.neg2abs_payments()
            #self.walkthrough_idxs('reduce_monopayments')# will be fixed soon
            #self.walkthrough_idxs('sum_eq_payments')
