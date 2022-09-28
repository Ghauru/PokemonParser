import urllib.request
from bs4 import BeautifulSoup
import re


def url_decode(url):
    try:
        return urllib.request.urlopen(url).read().decode('utf-8')
    except:
        return None


def parse_links_to_pages(body):
    page_count_func = 0
    for links in body.find_all('a'):
        if 'page' in str(links.get('href')):
            if page_count_func < int(re.findall('\d+', str(links.get('href')))[0]):
                page_count_func = int(re.findall('\d+', str(links.get('href')))[0])
    return page_count_func


def pokemon(pokemon_name, dictionary):
    print('Pokemon stats for ' + pokemon_name + ':')
    for key in dictionary.keys():
        if pokemon_name.lower() in key:
            return dictionary[key]


resp = url_decode('https://pokemongolife.ru/pokemony/')
soup = BeautifulSoup(resp, 'html.parser')
page_count = parse_links_to_pages(soup)
pages = []
pokemons = dict()


for i in range(1,page_count+1):
    pages.append('https://pokemongolife.ru/pokemony/page/' + str(i))
    resp_page = url_decode(pages[i-1])
    soup_page = BeautifulSoup(resp, 'html.parser')
    for info in soup_page.find_all('div', id='dle-content'):
        for a in info.find_all('a'):
            if 'pokemony' not in str(a.get('href')):
                pokemons[(str(a.get('href')))] = ''
                resp_pokemon = url_decode(str(a.get('href')))
                if resp_pokemon is not None:
                    soup_pokemon = BeautifulSoup(resp_pokemon, 'html.parser')
                    attrs = soup_pokemon.find_all("div", "pokemon-ability-info color-bg color-lightblue match active")[
                        0].find_all("li")
                    for li in attrs:
                        name = li.find("span", "attribute-title")
                        v = li.find("span", "attribute-value")
                        if name and v:
                            lis1 = [text for text in name.stripped_strings]
                            lis2 = [text for text in v.stripped_strings]
                            for k in lis1:
                                if k == 'Пол':
                                    if len(v.find_all('i')) > 1:
                                        pokemons[(str(a.get('href')))] += 'Пол: М/Ж' + ' '
                                    else:
                                        for pol in v.find_all('i'):
                                            if 'female' in str(pol):
                                                pokemons[(str(a.get('href')))] += 'Пол: Ж' + ' '
                                            else:
                                                pokemons[(str(a.get('href')))] += 'Пол: М' + ' '
                                else:
                                    pokemons[(str(a.get('href')))] += str(k) + ' '
                            for m in lis2:
                                pokemons[(str(a.get('href')))] += ': ' + str(m) + ' '