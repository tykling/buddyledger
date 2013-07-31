from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'buddyledger.views.CreateLedger'),
    url(r'^ledger/(?P<ledgerid>\d+)/$', 'buddyledger.views.ShowLedger'),
    url(r'^ledger/(?P<ledgerid>\d+)/edit/$', 'buddyledger.views.EditLedger'),
    url(r'^ledger/(?P<ledgerid>\d+)/addperson$', 'buddyledger.views.AddPerson'),
    url(r'^person/(?P<personid>\d+)/edit/$', 'buddyledger.views.EditPerson'),
    url(r'^person/(?P<personid>\d+)/remove/$', 'buddyledger.views.RemovePerson'),
    
    # Admin urls
    url(r'^admin/', include(admin.site.urls)),
)