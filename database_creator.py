import pymysql.cursors


def create(password):
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
                        title varchar(100),
                        date varchar(100));""")
        cur.execute("""CREATE TABLE game_score
                        (game_id int,
                        ranking int,
                        meta_score float,
                        user_score float,
                        FOREIGN KEY (game_id) REFERENCES game(id));""")
        cur.execute("""CREATE TABLE platform
                        (game_id int,
                        platform varchar(30),
                        FOREIGN KEY (game_id) REFERENCES game(id));""")
        cur.execute("""CREATE TABLE link_url
                        (game_id int,
                        metacritic_link varchar(255),
                        youtube_link varchar(255),
                        FOREIGN KEY (game_id) REFERENCES game(id));""")
    print('Database created.')
