from django.shortcuts import render
from .scripts.COVIDCrawler.covidCrawler import CovidScraper


def index(request):
    # Gets searched state
    searchedState = request.POST.get('searchedState')
    # Opens JSON file to check for states
    with open('./static/json/states.json', 'r') as stateList:
        x = stateList.read()
    # check to see if search bar includes a state
    if not searchedState == '' and searchedState is not None and searchedState.lower() in x.lower():
        if request.method == 'POST':
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
