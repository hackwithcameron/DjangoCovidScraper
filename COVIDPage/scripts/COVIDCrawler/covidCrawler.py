import requests
from bs4 import BeautifulSoup


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
    def stateScraper(self, searchedState):
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


