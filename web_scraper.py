import requests
from bs4 import BeautifulSoup
import os
import sys
import pandas as pd

REQUIRED_NUM_OF_ARGS = 3
POSSIBLE_CATEGORIES = ['Link', 'Rank', 'Title', 'Date', 'Platform', 'Meta_Score', 'User_Score', 'Game_Summary']


def abs_path_creator(input_path):
    """This function receives a path (absolute or relative) and processes it to be good for the use in the program
    It also creates a directory, in case it does not exist"""
    if not os.path.exists(input_path):
        os.mkdir(input_path)
    return os.path.abspath(input_path)


def dic_keys_creator(to_scrap):
    """This function receives a list and returns it with the string is the format of title"""
    d_keys = [key.title() for key in to_scrap]
    return d_keys


def dic_values_creator(dic_keys):
    """This function receives a list and returns another one with n empy lists, where n is the size of the imput list"""
    dic_values = [[] * k for k in range(len(dic_keys))]
    return dic_values


def main():

    if len(sys.argv) < REQUIRED_NUM_OF_ARGS:
        print("ERROR: Insufficient input.")
        print("usage: /web_scraper.py #pages Link Rank Title...)")
        sys.exit(1)
    try:
        pages_to_scrap = int(sys.argv[1])
        categories_to_scrap = sys.argv[2:]
        dic_key_list = dic_keys_creator(categories_to_scrap)
        for key in dic_key_list:
            if key not in POSSIBLE_CATEGORIES:
                print(f'ERROR: "{key}" data is not compatible with the data_scraper. Verify that your input is one of'
                      f' these available categories: {POSSIBLE_CATEGORIES}')
                raise SyntaxError
        dic_values_list = dic_values_creator(dic_key_list)
        dic = dict(zip(dic_key_list, dic_values_list))
        headers = {'User-Agent': ''}
        url = 'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page=0'
        for i in range(pages_to_scrap):
            page_url = url[0:len(url) - 1] + str(i)
            print(f'Downloading page_{i}...')
            test = requests.get(page_url, headers=headers)
            soup = BeautifulSoup(test.text, 'html.parser')
            for game in soup.find_all('td', class_="clamp-summary-wrap"):
                if "Link" in dic_key_list:
                    dic["Link"].append('https://www.metacritic.com' + str(game.find('a', class_="title")).split('\"')[3])
                if "Rank" in dic_key_list:
                    dic["Rank"].append(game.find('span', class_="title numbered").text.split()[0].strip('.'))
                if "Title" in dic_key_list:
                    dic["Title"].append(game.h3.text)
                if "Date" in dic_key_list:
                    dic["Date"].append(' '.join(game.find('div', class_="clamp-details").text.split()[-3:]))
                if "Platform" in dic_key_list:
                    dic["Platform"].append(' '.join(game.find('span', class_="data").text.split()))
                if "Meta_Score" in dic_key_list:
                    dic["Meta_Score"].append(game.find('div', class_="clamp-metascore").text.split()[1])
                if "User_Score" in dic_key_list:
                    dic["User_Score"].append(game.find('div', class_="clamp-userscore").text.split()[2])
                if "Game_Summary" in dic_key_list:
                    dic["Game_Summary"].append(' '.join(game.find('div', class_="summary").text.split()))
        df = pd.DataFrame(dic)
        print(df)
    except SyntaxError:
        sys.exit(1)
    except ValueError:
        print('ERROR: Incorrect input. The number of pages must be numerical.')
        sys.exit(1)

if __name__ == '__main__':
    main()
