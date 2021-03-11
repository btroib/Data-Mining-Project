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
                        link varchar(255),
                        title varchar(255),
                        date varchar(255),
                        platform varchar(255));""")
        cur.execute("""CREATE TABLE game_score
                        (game_id int REFERENCES game(id),
                        ranking int,
                        meta_score float,
                        user_score float);""")
    print('Database created.')
