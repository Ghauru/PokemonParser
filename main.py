from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import re


def url_decode(url):
    try:
        return urllib.request.urlopen(url).read().decode('utf-8')
    except:
        return None


def parse_links_to_pages(body):
    page_count_func = 0
    for a in body.find_all('a'):
        if 'page' in str(a.get('href')):
            if page_count_func < int(re.findall('\d+', str(a.get('href')))[0]):
                page_count_func = int(re.findall('\d+', str(a.get('href')))[0])
    return page_count_func


#def pokemon(pokemon_name):


resp = url_decode('https://pokemongolife.ru/pokemony/')
soup = BeautifulSoup(resp, 'html.parser')
page_count = parse_links_to_pages(soup)
pages = []
pokemons = dict()
pokemons_new = dict()


for i in range(1,page_count+1):
    pages.append('https://pokemongolife.ru/pokemony/page/' + str(i))
    resp = url_decode(pages[i-1])
    soup = BeautifulSoup(resp, 'html.parser')
    for info in soup.find_all('div', id='dle-content'):
        for a in info.find_all('a'):
            if 'pokemony' not in str(a.get('href')):
                pokemons[(str(a.get('href')))] = ''
                resp = url_decode(str(a.get('href')))
                if resp != None:
                    soup = BeautifulSoup(resp, 'html.parser')
                    attrs = soup.find_all("div", "pokemon-ability-info color-bg color-lightblue match active")[0].find_all("li")
                    for li in attrs:
                        name = li.find("span", "attribute-title")
                        v = li.find("span", "attribute-value")
                        if name and v:
                            pokemons[(str(a.get('href')))] = ''
                            lis1 = [text for text in name.stripped_strings]
                            lis2 = [text for text in v.stripped_strings]
                            for k in lis1:
                                if k == 'Пол':
                                    if len(v.find_all('i'))>1:
                                        pokemons[(str(a.get('href')))] += 'Пол : М/Ж'
                                    else:
                                        for pol in v.find_all('i'):
                                            if 'female' in str(pol):
                                                pokemons[(str(a.get('href')))] += 'Пол : Ж'
                                            else:
                                                pokemons[(str(a.get('href')))] += 'Пол : М'
                                else:
                                    pokemons[(str(a.get('href')))] += k
                            for k in lis2:
                                pokemons[(str(a.get('href')))] += ' : ' + k