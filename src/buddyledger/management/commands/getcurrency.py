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
                rate = int(rate * 100)

                try:
                    currency = Currency.objects.get(iso4217_code=child.attrib['code'])
                    currency.danish_ore_price=rate
                    temp = ""
                except Currency.DoesNotExist:
                    currency = Currency(iso4217_code=child.attrib['code'],danish_ore_price=rate)
                    temp = " new"
            
                currency.save()
                self.stdout.write('Saved%s rate: 100 %s costs %s danish ore' % (temp, child.attrib['code'],rate))
            else:
                self.stdout.write('Skipping currency %s - no price found' % child.attrib['code'])

        ### add DKK
        try:
            currency = Currency.objects.get(iso4217_code='DKK')
            currency.danish_ore_price=10000
            temp = ""
        except Currency.DoesNotExist:
            currency = Currency(iso4217_code='DKK',danish_ore_price=10000)
            temp = " new"
        currency.save()
        self.stdout.write('Saved%s rate: 100 DKK costs 10000 danish ore' % temp)

        self.stdout.write('Done.')
