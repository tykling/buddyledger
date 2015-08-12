from django.core.management.base import BaseCommand, CommandError
from buddyledger.models import Currency
from decimal import *
import urllib, json
import xml.etree.ElementTree as etree

try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen

class Command(BaseCommand):
    help = 'Gets currency exchange rates from nationalbanken'

    def handle(self, *args, **options):
        f = urlopen('http://www.nationalbanken.dk/_vti_bin/DN/DataService.svc/CurrencyRatesXML?lang=da')
        xml = f.read()
        f.close()
        tree = etree.fromstring(xml)
        for child in tree[0]:
            if child.attrib['rate'] != '-':
                rate = float(child.attrib['rate'].replace(".", "").replace(",", "."))/100

                try:
                    currency = Currency.objects.get(iso4217_code=child.attrib['code'])
                    currency.dkk_price=rate
                    temp = ""
                except Currency.DoesNotExist:
                    currency = Currency(iso4217_code=child.attrib['code'],dkk_price=rate)
                    temp = " new"
            
                currency.save()
                self.stdout.write('Saved%s rate: 1 %s costs %s DKK' % (temp, child.attrib['code'],rate))
            else:
                self.stdout.write('Skipping currency %s - no price found' % child.attrib['code'])


        ###########################################################################################
        ### add DKK
        try:
            currency = Currency.objects.get(iso4217_code='DKK')
            currency.dkk_price=1
            temp = ""
        except Currency.DoesNotExist:
            currency = Currency(iso4217_code='DKK',dkk_price=1)
            temp = " new"
        currency.save()
        self.stdout.write('Saved%s rate: 1 DKK costs 1 DKK ... ofcourse' % temp)

        ###########################################################################################
        self.stdout.write('Done getting currencies.')

