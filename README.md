# Django Covid-19 Dashboard

### Introduction
This was created for educational purposes. I created a web scraper using pythons requests library and Beautifulsoup, and decided to take it a little further by turning it into a local web application. By doing this I created a better layout and display the information in a more readable format. The web scraper itself can be found [here](https://github.com/hackwithcameron/DjangoCovidScraper/blob/master/COVIDPage/scripts/COVIDCrawler/covidCrawler.py) for this web application specifically.

### Demo
![](https://github.com/hackwithcameron/DjangoCovidScraper/blob/master/CovidSearch.gif)
<hr>

### Back-End stories
[Scraper (base)](#Scraping-with-BeautifulSoup(base))\
[Scraper (complete)](#Scraping-with-BeatutifulSoup-(complete))

### Front-End stories


<hr>

## Back-End

#### Scraping with BeautifulSoup(base)
To gather Information I chose to use Pythons requests library with BeautifulSoup. The target site [Worldometers US](https://www.worldometers.info/coronavirus/country/us/). This is the base scraper I created to get an idea of how to display the information gathered.
```
import requests
from bs4 import BeautifulSoup

searchedState = 'oregon'


# URL to be scraped
URL = 'https://www.worldometers.info/coronavirus/country/us/#nav-today'
statePage = requests.get(URL)
soup = BeautifulSoup(statePage.content, 'html.parser')
# Specifies table on page
table = soup.find(id='usa_table_countries_today')

# Gets header for list
def headerScraper():
    headers = table.find_all('th')

    headerInfo = []
    # Searches each cell to match state searched
    for header in headers:
        headerInfo.append(header.get_text(separator=" "))
    return headerInfo


# Gets searched states information
def stateScraper(searchedState):
    cells = table.find_all('td')

    stateInfo = []    # Empty list to hold parsed information
    for cell in cells:    # Searches each cell to match state searched
        if cell.text.strip().lower() == searchedState.lower():
            info = cell.find_next_siblings('td')      # Gets all 'td' cells up to the next 'tr'
            stateInfo.append(cell.text.strip())     # Append searched name to list
            for i in info:      # Gets information from each cell following the searched name
                if i.text.strip() == '' or i.text.strip() == '[*]':     # Replaces blank cells with a '0'
                    stateInfo.append('0')
                else:
                    stateInfo.append(i.text.strip())        # Appends information from cells following searched name
    return stateInfo

# Gets headers
headers = headerScraper()
# Gets searched states info
stateNumbers = stateScraper(searchedState)

results = list(zip(headers, stateNumbers))[:-5]    # Zips together lists, removes additional information for formatting

for display in results:
    print(display)
```
<hr>

#### Scraping with BeatutifulSoup(complete)
To get an idea of how to information was arranged and how to work with the data the above solution worked. But I wanted to be able to search the different states along with having a default if nothing was searched. That lead me to modify the exsisting scraped to look more like what is below. It also allowed me to pull from both "yesterdays" and "todays" tables to get both sets of information.
```
class CovidScraper:
    def __init__(self, tableTag):
        # URL to be scraped
        URL = 'https://www.worldometers.info/coronavirus/country/us/'
        statePage = requests.get(URL)
        soup = BeautifulSoup(statePage.content, 'html.parser')
        # Specifies table on page
        self.table = soup.find(id=tableTag)

    # Gets header for list
    def headerScraper(self):
        headers = self.table.find_all('th')

        headerInfo = []
        # Searches each cell to match state searched
        for header in headers:
            headerInfo.append(header.get_text(separator=" "))
        return headerInfo

    # Gets searched states information
    def stateScraper(self, searchedState='USA Total'):      # Sets default as 'USA Total' of nothing is searched
        cells = self.table.find_all('td')

        stateInfo = []    # Empty list to hold parsed information
        for cell in cells:    # Searches each cell to match state searched
            if cell.text.strip().lower() == searchedState.lower():
                info = cell.find_next_siblings('td')      # Gets all 'td' cells up to the next 'tr'
                stateInfo.append(cell.text.strip())     # Append searched name to list
                for i in info:      # Gets information from each cell following the searched name
                    if i.text.strip() == '':     # Replaces blank cells with a '0'
                        stateInfo.append('0')
                    else:
                        stateInfo.append(i.text.strip())        # Appends information from cells following searched name
        return stateInfo
```
<hr>

#### Views
Once I had the scraper built it was just a matter of linking it to my views and using the information it returned. Because I was using Django I added the scraper to a scripts folder in the app that was going to use it, then I just needed to import it into my views.py.
```
from django.shortcuts import render
from .scripts.COVIDCrawler.covidCrawler import CovidScraper


def index(request):
    # Gets searched state
    searchedState = request.POST.get('searchedState')
    
    # check to see if search bar includes a state
    if not (searchedState == '') and (searchedState is not None):
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
```
<hr>
To make sure what was searched is a US state I added the lines below to check for a match against a list of states as a json file.

```
# Opens JSON file to check for states
    with open('./static/json/states.json', 'r') as stateList:
        x = stateList.read()
```
along with an if statement to check for a match
```
if searchedState.lower() in x.lower():
```
<hr>

#### views.py complete
```
from django.shortcuts import render
from .scripts.COVIDCrawler.covidCrawler import CovidScraper


def index(request):
    # Gets searched state
    searchedState = request.POST.get('searchedState')
    # Opens JSON file to check for states
    with open('./static/json/states.json', 'r') as stateList:
        x = stateList.read()
    # check to see if search bar includes a state
    if not (searchedState == '') and (searchedState is not None):
        if searchedState.lower() in x.lower():
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
```

## Front-End
For the Front-End I used Bootstrap 4 for styling along with custom CSS and JavaScript. 

#### Search Bar
Being able to search for the desired state information is important to have the web app reach a more broad range of users.
To help reduce the risk of misspelled searches I wanted to create an autofill feild that included all the US states. This was achieved by including a json file that included a list of all the US states which was parsed then appended the information to options in that datalist html tag.
```
<form method="POST" class="searchBarContainer">
      {% csrf_token %}
      <input type="text" class="searchBar" placeholder="Search States" name="searchedState" id="searchBar" list="stateList">
      <datalist id="stateList"></datalist>
      <button type="submit" class="searchButton"><i class="fa fa-search"></i></button>
</form>
```

##### JavaScript
JavaScript to Parse and add information to datalist
```
// AutoFill search bar
var stateList = document.getElementById('stateList');

var request = new XMLHttpRequest();

request.onreadystatechange = function(response) {
    if (request.readyState === 4) {
        if (request.status === 200) {
            // Parse through JSON file
            var stateOptions = JSON.parse(request.responseText);

            // Loop over the JSON file
            stateOptions.forEach(element => {
                var state = document.createElement('option');
                state.value = element;
                stateList.appendChild(state);
            });
        }
    }
};

request.open('GET', './static/json/states.json', true);
request.send();

var dataList = document.getElementById('json-datalist');
var input = document.getElementById('ajax');
```

#### Cards
Once I had the information passed from my views to my index.html file displaying the information was as straight forward as using the indices for each peace of information.
```
 <div class="card" id="past">
    <img src="{% static 'images/VirusPic.png' %}" class="virus virusSmall" alt=" ">
    <div class="card-header pastHeader">
        <h2>{{headerInfo.0}}</h2>
        <h3>{{stateInfo.0}}</h3>
    </div>
    <div class="card-body">
        <h4 class="pastTag">Yesterday</h4>
        <div class="pastInfo">
            <p>{{headerInfo.1}}</p>
            <p>{{pastInfo.1}}</p>
        </div>
        <div class="pastInfo">
            <p>{{headerInfo.2}}</p>
            <p>{{pastInfo.2}}</p>
        </div>
        <div class="pastInfo">
            <p>{{headerInfo.3}}</p>
            <p>{{pastInfo.3}}</p>
        </div>
        <div class="pastInfo">
            <p>{{headerInfo.4}}</p>
            <p>{{pastInfo.4}}</p>
        </div>
        <div class="pastInfo">
            <p>{{headerInfo.5}}</p>
            <p>{{pastInfo.5}}</p>
        </div>
    </div>
</div>
<div class="card" id="current">
    <img src="{% static 'images/VirusPic.png' %}" class="virus virusBig" alt=" ">
    <div class="card-header currentHeader">
        <h1>{{headerInfo.0}}</h1>
        <h2>{{stateInfo.0}}</h2>
    </div>
    <div class="card-body">
        <h2 class="currentTag">Current</h2>
        <div class="info">
            <h3>{{headerInfo.1}}</h3>
            <h3>{{stateInfo.1}}</h3>
        </div>
        <div class="info">
            <h3>{{headerInfo.2}}</h3>
            <h3>{{stateInfo.2}}</h3>
        </div>
        <div class="info">
            <h3>{{headerInfo.3}}</h3>
            <h3>{{stateInfo.3}}</h3>
        </div>
        <div class="info">
            <h3>{{headerInfo.4}}</h3>
            <h3>{{stateInfo.4}}</h3>
        </div>
        <div class="info">
            <h3>{{headerInfo.5}}</h3>
            <h3>{{stateInfo.5}}</h3>
        </div>
    </div>
</div>
```
