import requests
from bs4 import BeautifulSoup
import pandas as pd
import argparse
import pymysql.cursors
from getpass import getpass
from tqdm import tqdm

REQUIRED_NUM_OF_ARGS = 3
POSSIBLE_CATEGORIES = ['Link', 'Rank', 'Title', 'Date', 'Platform', 'Meta_Score', 'User_Score', 'Game_Summary']
GAME_DATABASE = ['']
PLATFORM_DATABASE = ['']
GAME_SCORE_DATABASE = ['']
N_TRIPS_TO_COMMIT = 10000


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
        for i in range(self._pages_to_scrape):
            page_url = url[0:len(url) - 1] + str(i)
            print(f'Downloading page_{i}...')
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
        df = pd.DataFrame(self._dic)
        return df

    def create_database(self):
        password = getpass('Insert your MySQL password:')

        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password=f'{password}',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cur:
            cur.execute('DROP DATABASE IF EXISTS metacritic;')
            cur.execute('CREATE DATABASE metacritic;')
            cur.execute('USE metacritic;')
            cur.execute("""CREATE TABLE game
                        (id int PRIMARY KEY,
                        link varchar(255),
                        title varchar(255),
                        date varchar(255),
                        platform_id int REFERENCES platform(platform_id));""")
            cur.execute("""CREATE TABLE platform
                        (platform_id int PRIMARY KEY,
                        platform_name varchar(255));""")
            cur.execute("""CREATE TABLE game_score
                        (game_id int REFERENCES game(id),
                        ranking int,
                        meta_score float,
                        user_score float,
                        platform_id int REFERENCES platform(platform_id));""")
            print('database created')
        n_rows = len(self._dic['Rank'])
        for row in range(n_rows):
            if 'Link' in self._dic_keys:
                link_db = self._dic['Link'][row]
            if 'Title' in self._dic_keys:
                title_db = self._dic['Title'][row]
            if 'Date' in self._dic_keys:
                date_db = self._dic['Date'][row]
            if 'Game_Summary' in self._dic_keys:
                game_summary_db = self._dic['Game_Summary'][row]
            if 'Platform' in self._dic_keys:
                platform_name_db = self._dic['Platform'][row]
            if 'Game_Summary' in self._dic_keys:
                game_summary_db = self._dic['Game_Summary'][row]
            if 'Rank' in self._dic_keys:
                ranking_db = self._dic['Rank'][row]
            if 'Meta_Score' in self._dic_keys:
                meta_score_db = self._dic['Meta_Score'][row]
            if 'User_Score' in self._dic_keys:
                user_score_db = self._dic['User_Score'][row]
            with connection.cursor() as cur:
                cur.execute(f"""INSERT INTO game
                            (id, link, title, date, platform_id)
                            VALUES ("{row}", "{link_db}","{title_db}", "{date_db}", "{row}");""")
                cur.execute(f"""INSERT INTO platform
                                            (platform_id, platform_name)
                                            VALUES ("{row}", '{platform_name_db}');""")
                cur.execute(f"""INSERT INTO game_score
                                            (game_id, ranking, meta_score, user_score, platform_id)
                                            VALUES ("{row}", "{ranking_db}", "{meta_score_db}", "{user_score_db}", "{row}");""")
                if row % N_TRIPS_TO_COMMIT == 0:
                    connection.commit()
            connection.commit()


def parser():
    parser = argparse.ArgumentParser()
    cat_choices = ['Link', 'Rank', 'Title', 'Date', 'Platform', 'Meta_Score', 'User_Score', 'Game_Summary']

    parser.add_argument('--n', nargs="?", const=1, metavar='Number of pages',
                        help="Number of web pages to be scraped from Metacritic's Game website.", type=int)

    parser.add_argument('--cat', metavar='Data categories', choices=cat_choices,
                        help="Option to chose for scrapping", nargs='+', type=str.title, required=True)

    args = parser.parse_args()
    number_pages = args.n
    categories_to_scrape = args.cat
    return (number_pages, categories_to_scrape)


def main():
    inp = parser()
    scraper = DataScraper(inp[0], inp[1])
    print(scraper.scrape_metacritic())

    # for key in categories_to_scrape:
    #     if key not in POSSIBLE_CATEGORIES:
    #         raise argparse.ArgumentTypeError()
    # except argparse.ArgumentTypeError:
    #     print(f'Error: Category name does not match any of the possible categories.')
    # except argparse.ArgumentError:
    #     print('Incorrect input.')
    #     sys.exit(1)

    # if len(sys.argv) < REQUIRED_NUM_OF_ARGS:
    #     print("ERROR: Insufficient input.")
    #     print("usage: /web_scraper.py /output_path #pages Link Rank Title...)")
    #     print("usage: /web_scraper.py #pages Link Rank Title...)")
    #     sys.exit(1)
    # for key in dic_key_list:
    #     if key not in POSSIBLE_CATEGORIES:
    #         raise SyntaxError
    # except SyntaxError:
    #     sys.exit(1)
    # except ValueError:
    #     print('ERROR: Incorrect input. The number of pages must be numerical.')
    #     sys.exit(1)


if __name__ == '__main__':
    main()
