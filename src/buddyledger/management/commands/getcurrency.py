from django.core.management.base import BaseCommand, CommandError
from buddyledger.models import Currency
import urllib
import xml.etree.ElementTree as etree

class Command(BaseCommand):
    help = 'Gets currency exchange rates from http://nationalbanken.dk/dndk/valuta.nsf/valuta.xml'

    def handle(self, *args, **options):
        f = urllib.urlopen('http://nationalbanken.dk/dndk/valuta.nsf/valuta.xml')
        xml = f.read()
        f.close()
        tree = etree.fromstring(xml)
        for child in tree[0]:
            if child.attrib['rate'] != '-':
                rate = float(child.attrib['rate'].replace(".", "").replace(",", "."))

                try:
                    currency = Currency.objects.get(iso4217_code=child.attrib['code'])
                    currency.dkk_price_for_1=rate/100
                    temp = ""
                except Currency.DoesNotExist:
                    currency = Currency(iso4217_code=child.attrib['code'],dkk_price_for_1=rate)
                    temp = " new"
            
                currency.save()
                self.stdout.write('Saved%s rate: 1 %s costs %s DKK' % (temp, child.attrib['code'],rate))
            else:
                self.stdout.write('Skipping currency %s - no price found' % child.attrib['code'])

        ### add DKK
        try:
            currency = Currency.objects.get(iso4217_code='DKK')
            currency.dkk_price_for_1=1
            temp = ""
        except Currency.DoesNotExist:
            currency = Currency(iso4217_code='DKK',dkk_price_for_1=1)
            temp = " new"
        currency.save()
        self.stdout.write('Saved%s rate: 1 DKK costs 1 DKK ... ofcourse' % temp)

        self.stdout.write('Done.')
