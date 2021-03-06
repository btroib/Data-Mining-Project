import requests
from bs4 import BeautifulSoup
import os
import sys
import pandas as pd

REQUIRED_NUM_OF_ARGS = 3
POSSIBLE_CATEGORIES = ['Link', 'Rank', 'Title', 'Date', 'Platform', 'Meta_Score', 'User_Score', 'Game_Summary']


class Data_Scraper:

    def __init__(self):
        """
        Initiate the MetaCritic Data Scraper.
        """
        self.pages_to_scrape = pages_to_scrape
        self.dic_keys = dic_keys
        self.dic_values = dic_values
        self.dic = {}
        self.pages_to_scrape = pages_to_scrape

    def dic_keys_creator(self, pages_to_scrape):
        """This function receives a list and returns it with the string is the format of title"""
        dic_keys = [key.title() for key in pages_to_scrape]
        return dic_keys

    def dic_values_creator(self, dic_keys):
        """This function receives a list and returns another one with n empy lists, where n is the size of the imput list"""
        dic_values = [[] * k for k in range(len(dic_keys))]
        return dic_values

    def dic_creator(self, dic_keys, dic_values):
        """This function receives a list and returns another one with n empy lists, where n is the size of the imput list"""
        dic = dict(zip(dic_keys, dic_values))
        return dic

    def scrape_metacritic(self, pages_to_scrape, dic):
        """This function receives the number of pages to scrape, and returns another one with n empy lists, where n is the size of the imput list"""
        headers = {'User-Agent': ''}
        url = 'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page=0'
        for i in range(pages_to_scrape):
            page_url = url[0:len(url) - 1] + str(i)
            print(f'Downloading page_{i}...')
            requested_url = requests.get(page_url, headers=headers)
            parsed_url = Beautifulparsed_url(requested_url.text, 'html.parser')
            for game in parsed_url.find_all('td', class_="clamp-summary-wrap"):
                if "Link" in self.dic_keys:
                    dic["Link"].append('https://www.metacritic.com' + str(game.find('a', class_="title")).split('\"')[3])
                if "Rank" in self.dic_keys:
                    dic["Rank"].append(game.find('span', class_="title numbered").text.split()[0].strip('.'))
                if "Title" in self.dic_keys:
                    dic["Title"].append(game.h3.text)
                if "Date" in self.dic_keys:
                    dic["Date"].append(' '.join(game.find('div', class_="clamp-details").text.split()[-3:]))
                if "Platform" in self.dic_keys:
                    dic["Platform"].append(' '.join(game.find('span', class_="data").text.split()))
                if "Meta_Score" in self.dic_keys:
                    dic["Meta_Score"].append(game.find('div', class_="clamp-metascore").text.split()[1])
                if "User_Score" in self.dic_keys:
                    dic["User_Score"].append(game.find('div', class_="clamp-userscore").text.split()[2])
                if "Game_Summary" in self.dic_keys:
                    dic["Game_Summary"].append(' '.join(game.find('div', class_="summary").text.split()))
        df = pd.DataFrame(dic)
        return df

def main():

    if len(sys.argv) < REQUIRED_NUM_OF_ARGS:
        print("ERROR: Insufficient input.")
        print("usage: /web_scraper.py #pages Link Rank Title...)")
        sys.exit(1)
    try:
        pages_to_scrape = int(sys.argv[1])
        categories_to_scrape = sys.argv[2:]
        dic_keys = Data_Scraper.dic_keys_creator(categories_to_scrape, pages_to_scrape)
        dic_values = Data_Scraper.dic_values_creator(dic_keys)
        dic = Data_Scraper.dic_creator(dic_keys, dic_keys, dic_values)
        metacritic_df = Data_Scraper.scrape_metacritic(pages_to_scrape, dic)
        print(metacritic_df)
        for key in dic_keys:
            if key not in POSSIBLE_CATEGORIES:
                print(f'ERROR: "{key}" data is not compatible with the data_scraper. Verify that your input is one of'
                      f' these available categories: {POSSIBLE_CATEGORIES}')
                raise SyntaxError
        print(df)
    except SyntaxError:
        sys.exit(1)
    except ValueError:
        print('ERROR: Incorrect input. The number of pages must be numerical.')
        sys.exit(1)

if __name__ == '__main__':
    main()
