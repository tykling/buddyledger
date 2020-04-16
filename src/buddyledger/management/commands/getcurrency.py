import urllib, json
import xml.etree.ElementTree as etree
from decimal import *

try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen

def fetch():
    f = urlopen('https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml')
    xml = f.read()
    f.close()
    tree = etree.fromstring(xml)
    cube = tree[2][0]
    eur_rates = {}
    for child in cube:
        a = child.attrib
        rate = float(a['rate'])
        code = a['currency']
        eur_rates[code] = rate

    dkk_per_eur = 1 / eur_rates['DKK']

    for code, rate in eur_rates.items():
        if code == "DKK": continue
        yield code, rate * dkk_per_eur
    yield "EUR", dkk_per_eur

if __name__ == "__main__":
    import pprint, sys
    gen = fetch()
    pprint.pprint(list(gen))
    sys.exit(0)

from django.core.management.base import BaseCommand, CommandError
from buddyledger.models import Currency

class Command(BaseCommand):
    help = 'Gets currency exchange rates from nationalbanken'

    def handle(self, *args, **options):
        for code, rate in fetch():
            try:
                currency = Currency.objects.get(iso4217_code=code)
                currency.dkk_price = rate
                temp = ""
            except Currency.DoesNotExist:
                currency = Currency(iso4217_code=code, dkk_price=rate)
                temp = " new"

            self.stdout.write('Saved%s rate: 1 %s costs %s DKK' % (temp, code, rate))
            currency.save()


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
