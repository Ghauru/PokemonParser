from bs4 import BeautifulSoup
import my_functions as m
import sqlite3
import re


sqlite_connect = sqlite3.connect('pokemons.db')
sqlite_create_table = 'CREATE TABLE IF NOT EXISTS pokemons (id INTEGER PRIMARY KEY, name TEXT UNIQUE not null,' \
                        ' link TEXT UNIQUE not null, weight REAL, height REAL, gender TEXT, kind TEXT)'
cursor = sqlite_connect.cursor()
cursor.execute(sqlite_create_table)
cursor.close()


def pokemon_to_database(pokemon, index):
    weight = float(re.findall(r'-?\d+\.?\d*', pokemon.weight)[0])
    height = float(re.findall(r'-?\d+\.?\d*', pokemon.height)[0])
    sql_insert_query = f'INSERT INTO pokemons(name, link, weight, height, gender, kind) VALUES("{pokemon.name}",' \
                       f' "{pokemon.href}", "{weight}", "{height}", "{pokemon.gender}", "{pokemon.kind}")'
    cursor2 = sqlite_connect.cursor()
    try:
        cursor2.execute(sql_insert_query)
    except:
        sql_insert_query = f'UPDATE pokemons SET name = "{pokemon.name}", link = "{pokemon.href}",' \
                           f' weight = "{weight}", height = "{height}", gender = "{pokemon.gender}",' \
                           f' kind = "{pokemon.kind}" WHERE id = "{index}"'
        cursor2.execute(sql_insert_query)
    sqlite_connect.commit()
    cursor2.close()
    return index + 1


def delete_pokemon_db(index=None, name=None, link=None):
    cursor3 = sqlite_connect.cursor()
    if index:
        sql_insert_query = f'DELETE FROM pokemons WHERE id = "{index}"'
    elif name:
        sql_insert_query = f'DELETE FROM pokemons WHERE name = "{name}"'
    else:
        sql_insert_query = f'DELETE FROM pokemons WHERE link = "{link}"'
    try:
        cursor3.execute(sql_insert_query)
    except Exception as error:
        print(error)
    sqlite_connect.commit()
    cursor3.close()


def select_column(parameter):
    cursor4 = sqlite_connect.cursor()
    sql_insert_query = f'SELECT "{parameter}" from pokemons'
    print(list(cursor4.execute(sql_insert_query)))
    cursor4.close()


pokemon_index = 1
main_soup = BeautifulSoup(m.url_decode('https://pokemongolife.ru/pokemony/'), 'html.parser')
pages_count = m.parse_links_to_pages(main_soup)

links_to_pages = list(map(lambda x: 'https://pokemongolife.ru/pokemony/page/' + str(x) + '/', range(1, pages_count+1)))

for link_to_page in links_to_pages:
    resp_page = m.url_decode(link_to_page)
    links_to_pokemons = m.parse_links_to_pokemons(resp_page)
    for link_to_pokemon in links_to_pokemons.keys():
        pokemon_page_resp = m.url_decode(link_to_pokemon)
        new_pokemon = m.parse_pokemon_page(pokemon_page_resp, link_to_pokemon, links_to_pokemons[link_to_pokemon])
        pokemon_index = pokemon_to_database(new_pokemon, pokemon_index)
sqlite_connect.close()