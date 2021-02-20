import requests
from bs4 import BeautifulSoup
import os


# asking the the user the path where the files will be created
output_path = input("Enter the path of the directory where the files should be created (absolute or relative): ")

def abs_path_creator(input_path):
    """This function receives a path (absolute or relative) and processes it to be good for the use in the program
    It also creates a directory, in case it does not exist"""
    output_path_abs = os.path.abspath(input_path)
    if not os.path.exists(output_path_abs):
        os.mkdir(output_path_abs)
    return output_path_abs


# list with the dictionary keys
d_keys = ["Link", "Number", "Title", "Date", "Platform", "Meta Score", "User Score", "Game Summary"]


def dic_values_creator(dic_keys):
    dic_values = [[] * k for k in range(len(dic_keys))]
    return dic_values


values = dic_values_creator(d_keys)

dic = dict(zip(d_keys, values))

headers = {'User-Agent': ''}
url = 'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page=0'
for i in range(1):
    page_url = url[0:len(url) - 1] + str(i)
    print(f'page_{i}')
    test = requests.get(page_url, headers=headers)
    outfile = open(abs_path_creator(output_path) + f'/page_{i}.html', 'w')
    test.encoding = 'ISO-8859-1'
    outfile.write(str(test.text))
    with open(abs_path_creator(output_path) + f'/page_{i}.html') as html_file:
        soup = BeautifulSoup(html_file, 'lxml')
        for game in soup.find_all('td', class_="clamp-summary-wrap"):
            dic["Link"].append('https://www.metacritic.com' + str(game.find('a', class_="title")).split('\"')[3])
            dic["Number"].append(game.find('span', class_="title numbered").text.split()[0].strip('.'))
            dic["Title"].append(game.h3.text)
            dic["Date"].append(' '.join(game.find('div', class_="clamp-details").text.split()[-3:]))
            dic["Platform"].append(' '.join(game.find('span', class_="data").text.split()))
            dic["Meta Score"].append(game.find('div', class_="clamp-metascore").text.split()[1])
            dic["User Score"].append(game.find('div', class_="clamp-userscore").text.split()[2])
            dic["Game Summary"].append(' '.join(game.find('div', class_="summary").text.split()))
#' '.join
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
