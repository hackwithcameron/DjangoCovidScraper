from django.shortcuts import render
from .scripts.COVIDCrawler.covidCrawler import CovidScraper

# Toggle for running scraper
run = True


def index(request):
    if run:
        headerInfo = CovidScraper.headerScraper(CovidScraper(tableTag='nav-today'))
        stateInfo = CovidScraper.stateScraper(CovidScraper(tableTag='nav-today'), searchedState='Oregon')
        pastInfo = CovidScraper.stateScraper(CovidScraper(tableTag='nav-yesterday'), searchedState='Oregon')
        context = {
            "headerInfo": headerInfo,
            "stateInfo": stateInfo,
            "pastInfo": pastInfo
        }
        return render(request, 'COVIDPage/index.html', context)
    else:
        return render(request, 'COVIDPage/index.html')
