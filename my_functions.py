import urllib.request
from bs4 import BeautifulSoup
import re
from Pokemon import Pokemon


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


def parse_links_to_pokemons(body):
    soup = BeautifulSoup(body, 'html.parser')
    temp_dict = {}
    elems = soup.find_all("a", "soft3-item soft-fix")
    hrefs = list(map(lambda x: x.get('href'), elems))
    for elem in hrefs:
        temp_dict[elem] = elem[elem.find('-') + 1:elem.rfind('.')].title()
    return temp_dict


def parse_pokemon_page(body, href, pokemon_name):
    soup = BeautifulSoup(body, 'html.parser')
    attributes_block = soup.find_all("div", "pokemon-ability-info color-bg color-lightblue match active")[0]\
        .find_all("li")
    attributes = dict()
    for li in attributes_block:
        name = li.find("span", "attribute-title")
        value = li.find("span", "attribute-value")
        if name and value:
            attributes[name.get_text()] = value.get_text()
            attributes_list = [text for text in name.stripped_strings]
            for attribute in attributes_list:
                if attribute == 'Пол':
                    if len(value.find_all('i')) > 1:
                        attributes[name.get_text()] = 'М/Ж'
                    else:
                        for pol in value.find_all('i'):
                            if 'female' in str(pol):
                                attributes[name.get_text()] = 'Ж'
                            else:
                                attributes[name.get_text()] = 'М'

    pokemon = Pokemon()
    if 'Вес' in attributes:
        pokemon.weight = attributes['Вес']
    if 'Рост' in attributes:
        pokemon.height = attributes['Рост']
    if 'Пол' in attributes:
        pokemon.gender = attributes['Пол']
    if 'Вид' in attributes:
        pokemon.kind = attributes['Вид']

    pokemon.name = pokemon_name
    pokemon.href = href
    pokemon.pretty_info()
    return pokemon
