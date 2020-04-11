from django.shortcuts import render
from .scripts.COVIDCrawler.covidCrawler import *


def index(request):
    headerInfo = headerScraper()
    stateInfo = stateScraper('Oregon')
    context = {
        "headerInfo": headerInfo,
        "stateInfo": stateInfo
    }
    return render(request, 'COVIDPage/index.html', context)
