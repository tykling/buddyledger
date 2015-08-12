from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    ### frontpage and other static pages
    url(r'^$', 'buddyledger.views.Frontpage'),
    url(r'^usage/$', 'buddyledger.views.ShowUsage'),
    
    ### ledger
    url(r'^ledger/create/$', 'buddyledger.views.CreateLedger'),
    url(r'^ledger/(?P<ledgerid>\d+)/$', 'buddyledger.views.ShowLedger'),
    url(r'^ledger/(?P<ledgerid>\d+)/edit/$', 'buddyledger.views.EditLedger'),
    url(r'^ledger/(?P<ledgerid>\d+)/close/$', 'buddyledger.views.CloseLedger'),
    url(r'^ledger/(?P<ledgerid>\d+)/reopen/$', 'buddyledger.views.ReopenLedger'),

    ### person
    url(r'^ledger/(?P<ledgerid>\d+)/addperson/$', 'buddyledger.views.AddPerson'),
    url(r'^person/(?P<personid>\d+)/edit/$', 'buddyledger.views.EditPerson'),
    url(r'^person/(?P<personid>\d+)/remove/$', 'buddyledger.views.RemovePerson'),
    
    ### expense
    url(r'^ledger/(?P<ledgerid>\d+)/addexpense/$', 'buddyledger.views.AddExpense'),
    url(r'^expense/(?P<expenseid>\d+)/edit/$', 'buddyledger.views.EditExpense'),
    url(r'^expense/(?P<expenseid>\d+)/remove/$', 'buddyledger.views.RemoveExpense'),
    url(r'^expense/(?P<expenseid>\d+)/addperson/(?P<personid>\d+)/$', 'buddyledger.views.ExpenseAddPerson'),
    url(r'^expense/(?P<expenseid>\d+)/removeperson/(?P<personid>\d+)/$', 'buddyledger.views.ExpenseRemovePerson'),
)