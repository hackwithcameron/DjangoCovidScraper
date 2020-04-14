from django.shortcuts import render
from .scripts.COVIDCrawler.covidCrawler import *

# Toggle for running scraper
run = True


def index(request):
    if run:
        headerInfo = headerScraper()
        stateInfo = stateScraper('Oregon')
        context = {
            "headerInfo": headerInfo,
            "stateInfo": stateInfo
        }
        return render(request, 'COVIDPage/index.html', context)
    else:
        return render(request, 'COVIDPage/index.html')
