import re, datetime, os
from os import listdir
from os.path import isfile, join

import requests, bs4, PyPDF2
import numpy as np
import matplotlib.pyplot as plt

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from main import models

HOST_URL = 'http://localhost:8000'


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

        folder_fig_root = settings.MEDIA_ROOT+'fig/'
        folder_fig_url = HOST_URL+settings.MEDIA_URL+'fig/'
        if not os.path.exists(folder_fig_root):
            print('Creating folder: ' + folder_fig_root)
            os.makedirs(folder_fig_root)

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

                    labels = ['G1', 'G2', 'G3', 'G4', 'G5']
                    men_means = [20, 35, 30, 35, 27]
                    women_means = [25, 32, 34, 20, 25]
                    men_std = [2, 3, 4, 1, 2]
                    women_std = [3, 5, 2, 3, 3]
                    width = 0.35       # the width of the bars: can also be len(x) sequence

                    fig, ax = plt.subplots()

                    ax.bar(labels, men_means, width, yerr=men_std, label='Men')
                    ax.bar(labels, women_means, width, yerr=women_std, bottom=men_means,
                        label='Women')

                    ax.set_ylabel('Scores')
                    ax.set_title('Scores by group and gender')
                    ax.legend()

                    subpath = 'fig{}.png'.format(hash(
                        '{}-{}-{}'.format(year, month, day)+\
                            match['country']+match['cases_total']))
                    plt.savefig(folder_fig_root+subpath)
                    plt.close()
                    filetest = models.File.objects.create(
                        path=folder_fig_url+subpath
                    )

                    models.Report.objects.create(
                        date='{}-{}-{}'.format(year, month, day),
                        country=match['country'],
                        cases_total=match['cases_total'],
                        cases_new=match['cases_new'],
                        deaths_total=match['deaths_total'],
                        deaths_new=match['deaths_new'],
                        transmission_type=match['transmission_type'],
                        days_last_case=match['days_last_case'],
                        filetest=filetest
                    )
                