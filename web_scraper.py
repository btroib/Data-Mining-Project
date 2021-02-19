import requests
from bs4 import BeautifulSoup

game_links = []
game_numbered = []
game_title = []
game_date = []
game_platform = []
meta_score = []
user_score = []
game_summary = []
game_rating = []
headers = {'User-Agent': ''}
url = 'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page=0'
for i in range(183):
    page_url = url[0:len(url)-1]+str(i)
    print(f'page_{i}')
    test = requests.get(page_url, headers=headers)
    outfile = open(f'/Users/btroib/Desktop/Data_Mining_Project/pages_txt/page_{i}.html', 'w')
    test.encoding = 'ISO-8859-1'
    outfile.write(str(test.text))
    with open(f'/Users/btroib/Desktop/Data_Mining_Project/pages_txt/page_{i}.html') as html_file:
        soup = BeautifulSoup(html_file, 'lxml')
        for game in soup.find_all('td', class_="clamp-summary-wrap"):
            game_links.append('https://www.metacritic.com' + str(game.find('a', class_="title")).split('\"')[3])
            game_numbered.append(game.find('span', class_="title numbered").text.split()[0])
            game_title.append(game.h3.text)
            game_date.append(' '.join(game.find('div', class_="clamp-details").text.split()[3:]))
            game_platform.append(' '.join(game.find('span', class_="data").text.split()))
            meta_score.append(game.find('div', class_="clamp-metascore").text.split()[1])
            user_score.append(game.find('div', class_="clamp-userscore").text.split()[2])
            game_summary.append(' '.join(game.find('div', class_="summary").text.split()))
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

print(game_links)
print(game_numbered[0:10])
print(game_title[0:10])
print(game_date[0:10])
print(game_platform[0:10])
print(meta_score[0:10])
print(user_score[0:10])
print(game_summary[0:10])
