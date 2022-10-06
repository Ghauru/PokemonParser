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


class Pokemon:
    # вес, ссылка, рост, пол, вид, имя
    def __init__(self):
        self.weight = None
        self.href = None
        self.height = None
        self.gender = None
        self.kind = None
        self.name = None

    def pretty_info(self):
        print("Name: " + self.name, "Weight: " + self.weight, "Link: " + self.href, "Height: " + self.height, "Gender: " + self.gender,
              "Kind: " + self.kind, sep='\n')


main_soup = BeautifulSoup('https://pokemongolife.ru/pokemony/', 'html.parser')
pages_count = parse_links_to_pages(main_soup)

links_to_pages = list(map(lambda x: 'https://pokemongolife.ru/pokemony/page/' + str(x) + '/', range(1, pages_count)))

for link_to_page in links_to_pages:
    resp_page = url_decode(link_to_page)
    links_to_pokemons = parse_links_to_pokemons(resp_page)
    for link_to_pokemon in links_to_pokemons.keys():
        pokemon_page_resp = url_decode(link_to_pokemon)
        new_pokemon = parse_pokemon_page(pokemon_page_resp, link_to_pokemon, links_to_pokemons[link_to_pokemon])