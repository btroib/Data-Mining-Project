# scrape_metacritic configuration

METRACRITIC_URL = 'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page=0'

# add_to_database configuration
N_TRIPS_TO_COMMIT = 10000
HOST = 'localhost'
USER = 'root'
DATABASE = 'metacritic'

# youtube_trailer_finder configuration
SERVICE_NAME = 'youtube'
VERSION = 'v3'
API_KEY = ''  # to be filled in by the user

# Parser configuration
cat_choices = ['Link', 'Rank', 'Title', 'Date', 'Platform', 'Meta_Score', 'User_Score', 'Game_Summary']
