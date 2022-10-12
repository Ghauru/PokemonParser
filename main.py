from bs4 import BeautifulSoup
import my_functions as m


main_soup = BeautifulSoup(m.url_decode('https://pokemongolife.ru/pokemony/'), 'html.parser')
pages_count = m.parse_links_to_pages(main_soup)

links_to_pages = list(map(lambda x: 'https://pokemongolife.ru/pokemony/page/' + str(x) + '/', range(1, pages_count)))

for link_to_page in links_to_pages:
    resp_page = m.url_decode(link_to_page)
    links_to_pokemons = m.parse_links_to_pokemons(resp_page)
    for link_to_pokemon in links_to_pokemons.keys():
        pokemon_page_resp = m.url_decode(link_to_pokemon)
        new_pokemon = m.parse_pokemon_page(pokemon_page_resp, link_to_pokemon, links_to_pokemons[link_to_pokemon])