from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    ### frontpage and other static pages
    url(r'^$', 'buddyledger.views.Frontpage', name='frontpage'),
    url(r'^usage/$', 'buddyledger.views.ShowUsage', name='show_usage'),
    
    ### ledger
    url(r'^ledger/create/$', 'buddyledger.views.CreateLedger', name='create_ledger'),
    url(r'^ledger/(?P<ledgerid>\d+)/$', 'buddyledger.views.ShowLedger', name='show_ledger'),
    url(r'^ledger/(?P<ledgerid>\d+)/edit/$', 'buddyledger.views.EditLedger', name='edit_ledger'),
    url(r'^ledger/(?P<ledgerid>\d+)/close/$', 'buddyledger.views.CloseLedger', name='close_ledger'),
    url(r'^ledger/(?P<ledgerid>\d+)/reopen/$', 'buddyledger.views.ReopenLedger', name='reopen_ledger'),
    url(r'^ledger/(?P<ledgerid>\d+)/changemethod/$', 'buddyledger.views.ChangeMethod', name='change_ledger_method'),

    ### person
    url(r'^ledger/(?P<ledgerid>\d+)/addperson/$', 'buddyledger.views.AddPerson', name='add_person'),
    url(r'^person/(?P<personid>\d+)/edit/$', 'buddyledger.views.EditPerson', name='edit_person'),
    url(r'^person/(?P<personid>\d+)/remove/$', 'buddyledger.views.RemovePerson', name='remove_person'),
    
    ### expense
    url(r'^ledger/(?P<ledgerid>\d+)/addexpense/$', 'buddyledger.views.AddExpense', name='add_expense'),
    url(r'^expense/(?P<expenseid>\d+)/edit/$', 'buddyledger.views.EditExpense', name='edit_expense'),
    url(r'^expense/(?P<expenseid>\d+)/remove/$', 'buddyledger.views.RemoveExpense', name='remove_expense'),
    url(r'^expense/(?P<expenseid>\d+)/addperson/(?P<personid>\d+)/$', 'buddyledger.views.ExpenseAddPerson', name='expense_add_person'),
    url(r'^expense/(?P<expenseid>\d+)/removeperson/(?P<personid>\d+)/$', 'buddyledger.views.ExpenseRemovePerson', name='expense_remove_person'),
)