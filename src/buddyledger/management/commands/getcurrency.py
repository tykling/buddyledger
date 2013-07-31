from django.core.management.base import BaseCommand, CommandError
from buddyledger.models import Currency
import urllib

class Command(BaseCommand):
    help = 'Gets currency exchange rates from http://nationalbanken.dk/dndk/valuta.nsf/valuta.xml'

    def handle(self, *args, **options):
        tree = etree.parse('http://nationalbanken.dk/dndk/valuta.nsf/valuta.xml')
        root = tree.getroot()
        for child in root[0]:
            try:
                currency = Currency.objects.get(iso4217_code=child.attrib['code'])
                currency.danish_ore_price=child.attrib['rate']/100
            except Currency.DoesNotExist:
                currency = Currency(code=child.attrib['code'],danish_ore_price=child.attrib['rate']/100)
            
            currency.save()
            self.stdout.write('Saved rate: 100 %s costs %s danish ore' % (child.attrib['code'],child.attrib['rate']/100)
