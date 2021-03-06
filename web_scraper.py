import requests
from bs4 import BeautifulSoup
import os
import sys
import pandas as pd

REQUIRED_NUM_OF_ARGS = 3
POSSIBLE_CATEGORIES = ['Link', 'Rank', 'Title', 'Date', 'Platform', 'Meta_Score', 'User_Score', 'Game_Summary']


class Data_Scraper:

    def __init__(self, pages_to_scrape, categories):
        """
        Initiate the MetaCritic Data Scraper.
        """
        self._pages_to_scrape = pages_to_scrape
        self._categories = categories
        self._dic_keys = [key.title() for key in self._categories]
        self._dic_values = [[] * k for k in range(len(self._dic_keys))]
        self._dic = dict(zip(self._dic_keys, self._dic_values))

    def scrape_metacritic(self):
        """This function receives the number of pages to scrape, and returns another one with n empy lists, where n is the size of the imput list"""
        headers = {'User-Agent': ''}
        url = 'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page=0'
        for i in range(self._pages_to_scrape):
            page_url = url[0:len(url) - 1] + str(i)
            print(f'Downloading page_{i}...')
            requested_url = requests.get(page_url, headers=headers)
            parsed_url = BeautifulSoup(requested_url.text, 'html.parser')
            for game in parsed_url.find_all('td', class_="clamp-summary-wrap"):
                if "Link" in self._dic_keys:
                    self._dic["Link"].append('https://www.metacritic.com' + str(game.find('a', class_="title")).split('\"')[3])
                if "Rank" in self._dic_keys:
                    self._dic["Rank"].append(game.find('span', class_="title numbered").text.split()[0].strip('.'))
                if "Title" in self._dic_keys:
                    self._dic["Title"].append(game.h3.text)
                if "Date" in self._dic_keys:
                    self._dic["Date"].append(' '.join(game.find('div', class_="clamp-details").text.split()[-3:]))
                if "Platform" in self._dic_keys:
                    self._dic["Platform"].append(' '.join(game.find('span', class_="data").text.split()))
                if "Meta_Score" in self._dic_keys:
                    self._dic["Meta_Score"].append(game.find('div', class_="clamp-metascore").text.split()[1])
                if "User_Score" in self._dic_keys:
                    self._dic["User_Score"].append(game.find('div', class_="clamp-userscore").text.split()[2])
                if "Game_Summary" in self._dic_keys:
                    self._dic["Game_Summary"].append(' '.join(game.find('div', class_="summary").text.split()))
        df = pd.DataFrame(self._dic)
        return df

def main():

    number_pages = int(sys.argv[1])
    categories_to_scrape = sys.argv[2:]
    scraper = Data_Scraper(number_pages, categories_to_scrape)
    print(scraper.scrape_metacritic())

if __name__ == '__main__':
    main()