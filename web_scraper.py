import requests
from bs4 import BeautifulSoup
import os


# asking the the user the path where the files will be created
output_path = input("Enter the path of the directory where the files should be created (absolute or relative): ")
# this lines deals with relative and absolute paths
output_path_abs = os.path.abspath(output_path)
# if the given input directory does not exist, it will be created
if not os.path.exists(output_path_abs):
    os.mkdir(output_path_abs)

# list with the dictionary keys
dic_keys = ["Link", "Number", "Title", "Date", "Platform", "Meta Score", "User Score", "Game Summary"]
# list with internal lists that are the dictionary values
dic_values = [[]*i for i in range(len(dic_keys))]

headers = {'User-Agent': ''}
url = 'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page=0'
for i in range(5):
    page_url = url[0:len(url)-1]+str(i)
    print(f'page_{i}')
    test = requests.get(page_url, headers=headers)
    outfile = open(output_path_abs + f'/page_{i}.html', 'w')
    test.encoding = 'ISO-8859-1'
    outfile.write(str(test.text))
    with open(output_path_abs + f'/page_{i}.html') as html_file:
        soup = BeautifulSoup(html_file, 'lxml')
        for game in soup.find_all('td', class_="clamp-summary-wrap"):
            dic_values[0].append('https://www.metacritic.com' + str(game.find('a', class_="title")).split('\"')[3])
            dic_values[1].append(game.find('span', class_="title numbered").text.split()[0])
            dic_values[2].append(game.h3.text)
            dic_values[3].append(' '.join(game.find('div', class_="clamp-details").text.split()[3:]))
            dic_values[4].append(' '.join(game.find('span', class_="data").text.split()))
            dic_values[5].append(game.find('div', class_="clamp-metascore").text.split()[1])
            dic_values[6].append(game.find('div', class_="clamp-userscore").text.split()[2])
            dic_values[7].append(' '.join(game.find('div', class_="summary").text.split()))
            print(dic_values)

print(dic_values)
# creating a dictionary using the lists 'dic_keys' and 'key_values'
dic = dict(zip(dic_keys, dic_values))
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
