# Data_Mining_Project
***

## Web Scraper

### Description:
***

This program scrapes Metacritic's website for data regarding gaming. There are 182 pages on Metacritics gaming rank, each page contains 100 games from highest to lowest Metacritic ranking. The program will save each page in HTML format in an output path (absolute or relative) designated by the user. This web_scraper is capable of scraping the following data from each game: Link, Rank, Title, Date (release), Platform, Meta Score, User Score and Game Summary. You can choose how many web pages you request to scrape as well as which data to scrape for.

### Usage:
***
To run the Web_Scraper from the command line, the following initial input must be given:
```
python /web_scraper.py /output_path
```
The user must also add the number of pages and the category which should be scraped. See below a description of all possible commands:

| Command | Example |
| :-:  | ------ |
| 1** | Each page contains 100 games in descending order. In this case, one page of metacritic would be downloaded returning the 100 highest ranking games.  |
| Link | Will return you the game's Metacritic website URL.|
| Rank | The game's Metacritic ranking score.|
| Title | The game's title. |
| Date | The game's date of release. |
| Platform | The platform in which the game runs on. |
| Meta_Score | Meta_Score is Metacritics score given by professional reviews. |
| User_Score | User_Score is the score given by users on Metacritic. |
| Game_Summary | Provides a short summary of the game. |

 ** Number of pages is a required input with a minimum value of 1.

See below an example:
```
python /web_scraper.py /output_path 10 Rank Title Date
```
This command would result in the web_scraper downloading 10 pages and the categories of _Rank_, _Title_ and _Date_.

### Authors:
***

__André Gutnik__ & __Brian Troib__