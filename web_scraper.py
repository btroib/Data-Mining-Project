import requests
from bs4 import BeautifulSoup
import pandas as pd
import argparse
import pymysql.cursors
from getpass import getpass
import database_creator
import logging
from tqdm import tqdm

REQUIRED_NUM_OF_ARGS = 3
POSSIBLE_CATEGORIES = ['Link', 'Rank', 'Title', 'Date', 'Platform', 'Meta_Score', 'User_Score', 'Game_Summary']
GAME_DATABASE = ['']
PLATFORM_DATABASE = ['']
GAME_SCORE_DATABASE = ['']
N_TRIPS_TO_COMMIT = 10000

# Logging configuration
logging.basicConfig(filename='web_scraper.log', level=logging.INFO,
                    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s')


class DataScraper:

    def __init__(self, pages_to_scrape, categories):
        """
        Initiates an object from the class DataScraper
        :param pages_to_scrape: number of pages to scrape from Metacritic's website - int
        :param categories: list of categories to be scraped
        """
        self._pages_to_scrape = pages_to_scrape
        self._categories = categories
        self._dic_keys = [key.title() for key in self._categories]
        self._dic_values = [[] * k for k in range(len(self._dic_keys))]
        self._dic = dict(zip(self._dic_keys, self._dic_values))

    def scrape_metacritic(self):
        """Executes the website scrapping, storing the data in a dictionary and generating a DataFrame"""
        headers = {'User-Agent': ''}
        url = 'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page=0'
        for i in tqdm(range(self._pages_to_scrape)):
            page_url = url[0:len(url) - 1] + str(i)
            logging.info(f' Downloading page_{page_url}...')
            requested_url = requests.get(page_url, headers=headers)
            parsed_url = BeautifulSoup(requested_url.text, 'html.parser')
            for game in parsed_url.find_all('td', class_="clamp-summary-wrap"):
                if "Link" in self._dic_keys:
                    self._dic["Link"].append('https://www.metacritic.com' + str(game.find('a', class_="title"))
                                             .split('\"')[3])
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
                    if (game.find('div', class_="clamp-userscore").text.split()[2]) == 'tbd':
                        self._dic["User_Score"].append(0)
                    else:
                        self._dic["User_Score"].append(game.find('div', class_="clamp-userscore").text.split()[2])
                if "Game_Summary" in self._dic_keys:
                    self._dic["Game_Summary"].append(' '.join(game.find('div', class_="summary").text.split()))
        logging.info(f' Data Frame successfully created with {self._dic_keys}')
        df = pd.DataFrame(self._dic)
        return df

    def add_to_database(self, password):
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password=f'{password}',
                                     database='metacritic',
                                     cursorclass=pymysql.cursors.DictCursor)
        n_rows = len(self._dic[self._dic_keys[0]])
        for row in range(n_rows):
            if 'Link' in self._dic_keys:
                link_db = self._dic['Link'][row]
            else:
                link_db = 'NULL'
            if 'Title' in self._dic_keys:
                title_db = self._dic['Title'][row]
            else:
                title_db = 'NULL'
            if 'Date' in self._dic_keys:
                date_db = self._dic['Date'][row]
            else:
                date_db = 'NULL'
            if 'Platform' in self._dic_keys:
                platform_db = self._dic['Platform'][row]
            else:
                platform_db = 'NULL'
            if 'Rank' in self._dic_keys:
                ranking_db = self._dic['Rank'][row]
            else:
                ranking_db = 0
            if 'Meta_Score' in self._dic_keys:
                meta_score_db = self._dic['Meta_Score'][row]
            else:
                meta_score_db = 0
            if 'User_Score' in self._dic_keys:
                user_score_db = self._dic['User_Score'][row]
            else:
                user_score_db = 0
            with connection.cursor() as cur:
                cur.execute(f"""INSERT INTO game
                            (id, title, date)
                            VALUES ("{row}", "{title_db}", "{date_db}");""")
                cur.execute(f"""INSERT INTO platform
                            (game_id, platform)
                            VALUES ("{row}", "{platform_db}");""")
                cur.execute(f"""INSERT INTO link_url
                            (game_id, link)
                            VALUES ("{row}", "{link_db}");""")
                cur.execute(f"""INSERT INTO game_score
                            (game_id, ranking, meta_score, user_score)
                            VALUES ("{row}", "{ranking_db}", "{meta_score_db}", "{user_score_db}");""")
                cur.execute("""ALTER TABLE `game_score` ADD FOREIGN KEY (`game_id`) REFERENCES `game` (`id`);""")
                cur.execute("""ALTER TABLE `url_link` ADD FOREIGN KEY (`game_id`) REFERENCES `game` (`id`);""")
                cur.execute("""ALTER TABLE `platform` ADD FOREIGN KEY (`id`) REFERENCES `game` (`id`);""")
                if row % N_TRIPS_TO_COMMIT == 0:
                    connection.commit()
            connection.commit()


def parser():
    " Function that parsers the user input using argparse"
    parse = argparse.ArgumentParser()
    cat_choices = ['Link', 'Rank', 'Title', 'Date', 'Platform', 'Meta_Score', 'User_Score', 'Game_Summary']

    parse.add_argument('--n', nargs="?", const=1, metavar='Number of pages',
                       help="Number of web pages to be scraped from Metacritic's Game website.", type=int)

    parse.add_argument('--cat', metavar='Data categories', choices=cat_choices, help="Categories to be scraped.",
                       nargs='*', type=str.title, required=True)

    args = parse.parse_args()
    number_pages = args.n
    categories_to_scrape = args.cat
    if number_pages > 182:
        raise Exception

    if not categories_to_scrape:
        categories_to_scrape = ['Title', 'Rank']

    return number_pages, categories_to_scrape


def main():
    try:
        inp = parser()
        scraper = DataScraper(inp[0], inp[1])
        print(scraper.scrape_metacritic())
        password = getpass('Insert your MySQL password:')
        database_creator.create(password)
        scraper.add_to_database(password)
    except Exception:
        logging.error(" It is not possible to scrape more than 182 pages")


if __name__ == '__main__':
    main()

