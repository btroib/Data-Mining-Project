import requests
from bs4 import BeautifulSoup
import os
import sys


def abs_path_creator(input_path):
    """This function receives a path (absolute or relative) and processes it to be good for the use in the program
    It also creates a directory, in case it does not exist"""
    output_path_abs = os.path.abspath(input_path)
    if not os.path.exists(output_path_abs):
        os.mkdir(output_path_abs)
    return output_path_abs


def dic_keys_creator(to_scrap):
    """This function receives a list and returns it with the string is the format of title"""
    d_keys = [key.title() for key in to_scrap]
    return d_keys


def dic_values_creator(dic_keys):
    """This function receives a list and returns another one with n empy lists, where n is the size of the imput list"""
    dic_values = [[] * k for k in range(len(dic_keys))]
    return dic_values


def main():

    output_path = sys.path[1]
    pages_to_scrap = int(sys.path[2])
    categories_to_scrap = sys.path[3]

    abs_path = abs_path_creator(output_path)
    dic_key_list = dic_keys_creator(categories_to_scrap)
    dic_values_list = dic_values_creator(dic_key_list)

    dic = dict(zip(dic_key_list, dic_values_list))

    headers = {'User-Agent': ''}
    url = 'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page=0'
    for i in range(pages_to_scrap):
        page_url = url[0:len(url) - 1] + str(i)
        print(f'page_{i}')
        test = requests.get(page_url, headers=headers)
        outfile = open(abs_path + f'/page_{i}.html', 'w')
        test.encoding = 'ISO-8859-1'
        outfile.write(str(test.text))
        with open(abs_path + f'/page_{i}.html') as html_file:
            soup = BeautifulSoup(html_file, 'lxml')
            for game in soup.find_all('td', class_="clamp-summary-wrap"):
                if "Link" in categories_to_scrap:
                    dic["Link"].append('https://www.metacritic.com' + str(game.find('a', class_="title")).split('\"')[3])
                if "Number" in categories_to_scrap:
                    dic["Number"].append(game.find('span', class_="title numbered").text.split()[0].strip('.'))
                if "Title" in categories_to_scrap:
                    dic["Title"].append(game.h3.text)
                if "Date" in categories_to_scrap:
                    dic["Date"].append(' '.join(game.find('div', class_="clamp-details").text.split()[-3:]))
                if "Platform" in categories_to_scrap:
                    dic["Platform"].append(' '.join(game.find('span', class_="data").text.split()))
                if "Meta Score" in categories_to_scrap:
                    dic["Meta Score"].append(game.find('div', class_="clamp-metascore").text.split()[1])
                if "User Score" in categories_to_scrap:
                    dic["User Score"].append(game.find('div', class_="clamp-userscore").text.split()[2])
                if "Game Summary" in categories_to_scrap:
                    dic["Game Summary"].append(' '.join(game.find('div', class_="summary").text.split()))
    print(dic)







# i = 0
# for game in game_links:
#     print(i)
#     page = requests.get(game, headers=headers)
#     outfile = open(f'/Users/btroib/Desktop/Data_Mining_Project/pages_txt/game_{i}.html', 'w')
#     page.encoding = 'ISO-8859-1'
#     outfile.write(str(page.text))

# for i in range(0,1):
#     with open(f'/Users/btroib/Desktop/Data_Mining_Project/pages_txt/game_{i}.html') as html_file:
#         soup = BeautifulSoup(html_file, 'lxml')
#         for details in soup.find_all('div', class_="details side_details"):
#             game_rating.append(str(details.find('span', class_="data")).split())
#     i += 1
