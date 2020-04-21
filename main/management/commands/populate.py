import re, datetime
from os import listdir
from os.path import isfile, join

import requests, bs4, PyPDF2

from django.core.management.base import BaseCommand, CommandError
from main import models


def tupleToDict(t, y, m , d):
    return {
        'date': datetime.date(y, m, d),
        'country': t[0],
        'cases_total': t[1],
        'cases_new': t[2],
        'deaths_total': t[3],
        'deaths_new': t[4],
        'transmission_type': t[5],
        'days_last_case': t[6]
    }


class Command(BaseCommand):

    # extraparam: append option
    def add_arguments(self, parser):
        parser.add_argument('-d', '--delete', action='store_true')


    def handle(self, *args, **options):
        country_regex = '\s+([\w ]+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\w ]+)\s+(\d+)'
        date_regex = '(\d{4})(\d{2})(\d{2})'

        # print('options: ', options)
        if options['delete']:
            models.Report.objects.all().delete()

        folder = 'reports'
        files = [f for f in listdir(folder) if isfile(join(folder, f))]
        print('Mining data only after March 10th, 2020.')
        for file in files:
            year, month, day = re.findall(date_regex, file)[0]
            year, month, day = int(year), int(month), int(day)
            if year > 2020 or \
                (year == 2020 and (month > 3 \
                    or (month == 3 and day >= 11))):
                pdfFileObj = open('{}/{}'.format(folder, file), 'rb')
                pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                text = ''
                for page in range(pdfReader.numPages):
                    pageObj = pdfReader.getPage(page)
                    text += pageObj.extractText()
                matches = re.findall(country_regex, text)
                matches = [tupleToDict(match, year, month, day) for match in matches]
                print(year, month, day, len(matches))
                for match in matches:
                    models.Report.objects.create(
                        date='{}-{}-{}'.format(year, month, day),
                        country=match['country'],
                        cases_total=match['cases_total'],
                        cases_new=match['cases_new'],
                        deaths_total=match['deaths_total'],
                        deaths_new=match['deaths_new'],
                        transmission_type=match['transmission_type'],
                        days_last_case=match['days_last_case']
                    )