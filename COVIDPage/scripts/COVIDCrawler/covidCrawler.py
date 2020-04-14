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
                if i.text.strip() == '':     # Replaces blank cells with a '0'
                    stateInfo.append('0')
                else:
                    stateInfo.append(i.text.strip())        # Appends information from cells following searched name
    return stateInfo


