from django.conf.urls import include, re_path
from . import views

urlpatterns = [
    ### frontpage and other static pages
    re_path(r'^$', views.Frontpage, name='frontpage'),
    re_path(r'^usage/?$', views.ShowUsage, name='show_usage'),
    
    ### ledger
    re_path(r'^ledger/create/?$', views.CreateLedger, name='create_ledger'),
    re_path(r'^ledger/(?P<ledgerid>\d+)/?$', views.ShowLedger, name='show_ledger'),
    re_path(r'^ledger/(?P<ledgerid>\d+)/edit/?$', views.EditLedger, name='edit_ledger'),
    re_path(r'^ledger/(?P<ledgerid>\d+)/close/?$', views.CloseLedger, name='close_ledger'),
    re_path(r'^ledger/(?P<ledgerid>\d+)/reopen/?$', views.ReopenLedger, name='reopen_ledger'),
    re_path(r'^ledger/(?P<ledgerid>\d+)/changemethod/?$', views.ChangeMethod, name='change_ledger_method'),

    ### person
    re_path(r'^ledger/(?P<ledgerid>\d+)/addperson/?$', views.AddPerson, name='add_person'),
    re_path(r'^person/(?P<personid>\d+)/edit/?$', views.EditPerson, name='edit_person'),
    re_path(r'^person/(?P<personid>\d+)/remove/?$', views.RemovePerson, name='remove_person'),
    
    ### expense
    re_path(r'^ledger/(?P<ledgerid>\d+)/addexpense/?$', views.AddExpense, name='add_expense'),
    re_path(r'^expense/(?P<expenseid>\d+)/edit/?$', views.EditExpense, name='edit_expense'),
    re_path(r'^expense/(?P<expenseid>\d+)/remove/?$', views.RemoveExpense, name='remove_expense'),
    re_path(r'^expense/(?P<expenseid>\d+)/addperson/(?P<personid>\d+)/?$', views.ExpenseAddPerson, name='expense_add_person'),
    re_path(r'^expense/(?P<expenseid>\d+)/removeperson/(?P<personid>\d+)/?$', views.ExpenseRemovePerson, name='expense_remove_person'),
]