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
            try:
                currency = Currency.objects.get(iso4217_code=child.attrib['code'])
                currency.danish_ore_price=child.attrib['rate']/100
                temp = ""
            except Currency.DoesNotExist:
                currency = Currency(code=child.attrib['code'],danish_ore_price=child.attrib['rate']/100)
                temp = " new"
            
            currency.save()
            self.stdout.write('Saved%s rate: 100 %s costs %s danish ore' % (temp, child.attrib['code'],child.attrib['rate']/100))
