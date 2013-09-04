from django.core.management.base import BaseCommand, CommandError
from buddyledger.models import Currency
from Decimal import *
import urllib, json
import xml.etree.ElementTree as etree

class Command(BaseCommand):
    help = 'Gets currency exchange rates from http://nationalbanken.dk/dndk/valuta.nsf/valuta.xml and BTC rates from Bitstamp'

    def handle(self, *args, **options):
        f = urllib.urlopen('http://nationalbanken.dk/dndk/valuta.nsf/valuta.xml')
        xml = f.read()
        f.close()
        tree = etree.fromstring(xml)
        ### initialize usdprice variable (needed for btc price conversion later)
        usdprice = Decimal(0)
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
                if child.attrib['code'] = "USD":
                    ### save usd rate for later
                    usdprice = Decimal(rate)
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
        if usdprice != 0:
        ### if we have a USD/BTC rate, add BTC price based on bitstamp USD ticker
            try:
                f = urllib.urlopen('https://www.bitstamp.net/api/ticker/')
                bitstampjson = f.read()
                jsonobj = json.loads(bitstampjson)
                f.close()
            except Exception as e:
                self.stdout.write('Unable to get BTC price from https://www.bitstamp.net/api/ticker/')
            
            ### calculate DKK price from USD price
            btcusdprice = Decimal(jsonobj['last'])
            btcdkkprice = btcusdprice * usdprice
            
            try:
                currency = Currency.objects.get(iso4217_code='BTC')
                currency.dkk_price = btcdkkprice
                temp = ""
            except Currency.DoesNotExist:
                currency = Currency(iso4217_code='BTC',dkk_price=btcdkkprice)
                temp = " new"
            self.stdout.write('Saved%s rate: 1 BTC costs %s DKK' % temp)
        
        
        ###########################################################################################
        self.stdout.write('Done getting currencies.')

