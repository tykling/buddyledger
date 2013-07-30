from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^/$', 'ledger.views.CreateLedger'),
    url(r'^/ledger/(?P<ledgerid>\d+)/$', 'ledger.views.ShowLedger'),
    url(r'^/ledger/(?P<ledgerid>\d+)/edit/$', 'ledger.views.edit'),
    # Admin urls
    url(r'^admin/', include(admin.site.urls)),
)