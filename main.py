from bs4 import BeautifulSoup
import my_functions as m
import sqlite3


sqlite_connect = sqlite3.connect('pokemons.db')
sqlite_create_table = 'CREATE TABLE IF NOT EXISTS pokemons (id INTEGER PRIMARY KEY, name TEXT UNIQUE not null,' \
                        ' link TEXT UNIQUE not null, weight INTEGER , height INTEGER, gender TEXT not null, kind TEXT not null)'
cursor = sqlite_connect.cursor()
cursor.execute(sqlite_create_table)
cursor.close()
sqlite_connect.close()


def pokemon_to_database(pokemon):
    sqlite_connection = sqlite3.connect('pokemons.db')
    cur = sqlite_connection.cursor()
    cur.execute('PRAGMA table_info("pokemons")')
    column_names = [i[1] for i in cur.fetchall()]
    for i in range(1, len(column_names)):
        print('i= ' + pokemon.stats()[i-1])
        sql_insert_query = "INSERT INTO pokemons(" + column_names[i] + ") VALUES('{}')".format(pokemon.stats()[i-1])
        cur.execute(sql_insert_query)
        sqlite_connection.commit()
    cur.close()
    sqlite_connection.close()


main_soup = BeautifulSoup(m.url_decode('https://pokemongolife.ru/pokemony/'), 'html.parser')
pages_count = m.parse_links_to_pages(main_soup)

links_to_pages = list(map(lambda x: 'https://pokemongolife.ru/pokemony/page/' + str(x) + '/', range(1, pages_count)))

for link_to_page in links_to_pages:
    resp_page = m.url_decode(link_to_page)
    links_to_pokemons = m.parse_links_to_pokemons(resp_page)
    for link_to_pokemon in links_to_pokemons.keys():
        pokemon_page_resp = m.url_decode(link_to_pokemon)
        new_pokemon = m.parse_pokemon_page(pokemon_page_resp, link_to_pokemon, links_to_pokemons[link_to_pokemon])
        pokemon_to_database(new_pokemon)