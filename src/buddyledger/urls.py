from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    ### frontpage and other pages
    url(r'^$', 'buddyledger.presentation.Frontpage'),
    url(r'^usage/$', 'buddyledger.presentation.ShowUsage'),
    
    ### ledger
    url(r'^ledger/create/$', 'buddyledger.ledger.CreateLedger'),
    url(r'^ledger/(?P<ledgerid>\d+)/$', 'buddyledger.ledger.ShowLedger'),
    url(r'^ledger/(?P<ledgerid>\d+)/edit/$', 'buddyledger.ledger.EditLedger'),
    url(r'^ledger/(?P<ledgerid>\d+)/close/$', 'buddyledger.ledger.CloseLedger'),

    ### person
    url(r'^ledger/(?P<ledgerid>\d+)/addperson/$', 'buddyledger.person.AddPerson'),
    url(r'^person/(?P<personid>\d+)/edit/$', 'buddyledger.person.EditPerson'),
    url(r'^person/(?P<personid>\d+)/remove/$', 'buddyledger.person.RemovePerson'),
    
    ### expense
    url(r'^ledger/(?P<ledgerid>\d+)/addexpense/$', 'buddyledger.expense.AddExpense'),
    url(r'^expense/(?P<expenseid>\d+)/edit/$', 'buddyledger.expense.EditExpense'),
    url(r'^expense/(?P<expenseid>\d+)/remove/$', 'buddyledger.expense.RemoveExpense'),
    url(r'^expense/(?P<expenseid>\d+)/addperson/(?P<personid>\d+)/$', 'buddyledger.expense.ExpenseAddPerson'),
    url(r'^expense/(?P<expenseid>\d+)/removeperson/(?P<personid>\d+)/$', 'buddyledger.expense.ExpenseRemovePerson'),

    ### payments
    url(r'^expense/(?P<expenseid>\d+)/addpayment/$', 'buddyledger.payment.AddPayment'),
    url(r'^payment/(?P<paymentid>\d+)/edit/$', 'buddyledger.payment.EditPayment'),
    url(r'^payment/(?P<paymentid>\d+)/remove/$', 'buddyledger.payment.RemovePayment'),
)