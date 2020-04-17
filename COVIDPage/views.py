from django.shortcuts import render
from .scripts.COVIDCrawler.covidCrawler import CovidScraper

# Toggle for running scraper
run = True


def index(request):
    searchedState = request.POST.get('searchedState')
    if not (searchedState == ''):
        if request.method == 'POST':
            searchedState = request.POST.get('searchedState')
            headerInfo = CovidScraper.headerScraper(CovidScraper(tableTag='nav-today'))
            stateInfo = CovidScraper.stateScraper(CovidScraper(tableTag='nav-today'), searchedState=searchedState)
            pastInfo = CovidScraper.stateScraper(CovidScraper(tableTag='nav-yesterday'), searchedState=searchedState)
            context = {
                "headerInfo": headerInfo,
                "stateInfo": stateInfo,
                "pastInfo": pastInfo
            }
            return render(request, 'COVIDPage/index.html', context)

    else:
        headerInfo = CovidScraper.headerScraper(CovidScraper(tableTag='nav-today'))
        stateInfo = CovidScraper.stateScraper(CovidScraper(tableTag='nav-today'))
        pastInfo = CovidScraper.stateScraper(CovidScraper(tableTag='nav-yesterday'))
        context = {
            "headerInfo": headerInfo,
            "stateInfo": stateInfo,
            "pastInfo": pastInfo
        }
        return render(request, 'COVIDPage/index.html', context)
