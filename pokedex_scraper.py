import requests, json
from bs4 import BeautifulSoup
from pokemon import Pokemon, PokemonVariation
from pokemon import LEGENDARY_AND_MYTHICAL_POKEMON


POKEDEX_URL = 'https://pokemondb.net/pokedex/all'
POKEMON_DETAILS_URL = 'https://pokemondb.net/pokedex/'

def scrape_pokemon_data():
    response = requests.get(POKEDEX_URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    pokemon_list = []

    for pokemon in soup.find_all('tr')[1:]:  # Skip the header row
        columns = pokemon.find_all('td')
        pokedex_number = int(columns[0].text.strip())
        unparsed_name = columns[1].text.strip()
        type_tags = columns[2].find_all('a')
        types = [type_tag.text for type_tag in type_tags]

        existing_pokemon = next((existing_pokemon for existing_pokemon in pokemon_list if existing_pokemon.id == pokedex_number), None)

        if existing_pokemon:
            variation = create_pokemon_variation(unparsed_name, types)
            print("pokemon: " + existing_pokemon.name)
            existing_pokemon.add_variation(variation)
        else:
            pokemon = create_pokemon(pokedex_number, unparsed_name, types)
            pokemon_list.append(pokemon)

    return pokemon_list


def create_pokemon(pokedex_number, name, types):
    print("pokemon: " + name)
    response = requests.get(POKEMON_DETAILS_URL + name)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get pokemon image url
    image_url = soup.find('a', attrs=lambda attrs: attrs and 'data-title' in attrs and 'official artwork' in attrs['data-title']).find('img')['src']

    # Get pokemon height and weight
    vitals_table = soup.find('table', class_='vitals-table')

    height_row = vitals_table.find('th', string='Height')
    if height_row:
        height = height_row.find_next_sibling('td').string.strip().split('m')[0]
    else:
        height = None

    weight_row = vitals_table.find('th', string='Weight')
    if weight_row:
        weight = weight_row.find_next_sibling('td').string.strip().split('kg')[0]
    else:
        weight = None

    # Get pokemon category
    category_row = vitals_table.find('th', string='Species')
    if category_row:
        category = category_row.find_next_sibling('td').string.strip()
    else:
        weight = None

    # Get pokemon abilities
    abilities_row = vitals_table.find('th', string='Abilities')
    if abilities_row:
        abilities_tags = abilities_row.find_next_sibling('td').find_all('a', href=lambda href: href and '/ability/' in href)
        abilities = [ability_tag.text.strip() for ability_tag in abilities_tags]
    else:
        abilities = None
    
    # Get pokemon moves
    moves = get_moves_data(soup)

     # Get pokemon evolution stage
    evolution_stage = calculate_evolution_stage(soup, name)

    # Get pokemon legendary status
    legendary_status = name in LEGENDARY_AND_MYTHICAL_POKEMON

    # Create pokemon object with the scraped data
    pokemon = Pokemon(
        id=pokedex_number,
        name=name,
        types=types,
        height=height,
        weight=weight,
        category=category,
        abilities=abilities,
        moves=moves,
        evolution_stage=evolution_stage,
        imageUrl=image_url,
        legendaryStatus=legendary_status
    )

    return pokemon


def get_moves_data(soup):
    moves_data = {}

    # Moves learnt by level up
    level_up_moves_table = soup.find('h3', string='Moves learnt by level up').find_next('table', class_='data-table')
    if level_up_moves_table:
        level_up_moves = [move.string.strip() for move in level_up_moves_table.find_all('a', class_='ent-name')]
        moves_data['level_up_moves'] = level_up_moves

    # Moves learnt by TM
    tm_moves_table = soup.find('h3', string='Moves learnt by TM').find_next('table', class_='data-table')
    if tm_moves_table:
        tm_moves = [move.string.strip() for move in tm_moves_table.find_all('a', class_='ent-name')]
        moves_data['tm_moves'] = tm_moves
    
    # Egg moves
    egg_moves_table = soup.find('h3', string='Egg moves').find_next('table', class_='data-table')
    if egg_moves_table:
        egg_moves = [move.string.strip() for move in egg_moves_table.find_all('a', class_='ent-name')]
        moves_data['egg_moves'] = egg_moves

    # Moves learnt on evolution
    evolution_moves_title = soup.find('h3', string='Moves learnt on evolution')
    if evolution_moves_title:
        evolution_moves_table = evolution_moves_title.find_next('table', class_='data-table') 
        evolution_moves = [move.string.strip() for move in evolution_moves_table.find_all('a', class_='ent-name')]
        moves_data['evolution_moves'] = evolution_moves

    # Moves learned by Tutor
    evolution_moves_title = soup.find('h3', string='Moves Tutor moves')
    if evolution_moves_title:
        evolution_moves_table = evolution_moves_title.find_next('table', class_='data-table')
        evolution_moves = [move.string.strip() for move in evolution_moves_table.find_all('a', class_='ent-name')]
        moves_data['evolution_moves'] = evolution_moves

    return moves_data
    

def calculate_evolution_stage(soup, name):
    evolution_chart = soup.find('div', class_='infocard-list-evo')

    if evolution_chart:
        evolution_stages = evolution_chart.find_all('a', class_='ent-name')
        if evolution_stages:
            stage_counter = 1
            for evolution in evolution_stages:
                pokemon_name = evolution.string.strip()
                if pokemon_name == name:
                    return stage_counter
                stage_counter += 1

    return None


def create_pokemon_variation(unparsed_name, types):
    # Case for alternate form: Darmanitan
    if "Darmanitan" in unparsed_name:
        if "Standard" in unparsed_name:
            if "Galarian" in unparsed_name:
                variation_name = "Darmanitan Galarian Standard Mode"
            else:
                variation_name = "Darmanitan Standard Mode"
        elif "Zen" in unparsed_name:
            if "Galarian" in unparsed_name:
                variation_name = "Darmanitan Galarian Zen Mode"
            else:
                variation_name = "Darmanitan Zen Mode"

    # Case for alternate form: Basculin
    elif "Blue-Striped" in unparsed_name:
        variation_name = "Basculin Blue-Striped"
    elif "White-Striped" in unparsed_name:
        variation_name = "Basculin White-Striped"
    elif "Red-Striped" in unparsed_name:
        variation_name = "Basculin Red-Striped"

    # Case for alternate form: Tauros
    elif "Tauros" in unparsed_name:
        if "Combat" in unparsed_name:
            variation_name = "Tauros Combat Breed"
        elif "Blaze" in unparsed_name:
            variation_name = "Tauros Blaze Breed"
        elif "Aqua" in unparsed_name:
            variation_name = "Tauros Aqua Breed"
    
    elif "Partner" in unparsed_name:
        return None

    # Case for Mega 
    elif "Mega" in unparsed_name and unparsed_name != "Meganium":
        unparsed_variation_name = unparsed_name.split(" Mega", 1)
        variation_name = 'Mega' + unparsed_variation_name[1]
    
    # Case for Paldean Pokemon
    elif "Paldean" in unparsed_name:
        unparsed_variation_name = unparsed_name.split(" Paldean", 1)
        variation_name = 'Paldean' + unparsed_variation_name[1]

    # Case for Alolan
    elif "Alolan" in unparsed_name:
        unparsed_variation_name = unparsed_name.split(" Alolan ", 1)
        variation_name = 'Alolan' + unparsed_variation_name[1]

    # Case for Galarian
    elif "Galarian" in unparsed_name:
        unparsed_variation_name = unparsed_name.split(" Galarian ", 1)
        variation_name = 'Galarian' + unparsed_variation_name[1]
    
    variation = PokemonVariation(
        name=variation_name,
        types=types,
        imageUrl=""
    )

    return variation


def main():
    # p = create_pokemon(6, "Charizard", ["Fire", "Flying"])
    # pokemon_data = [p.to_dict()]

    # # Serialize to JSON and write to a file
    # with open('pokemon_data.json', 'w', encoding='utf-8') as f:
    #     json.dump(pokemon_data, f, ensure_ascii=False, indent=4)

    pokemon_list = scrape_pokemon_data()

    # Print the first 5 pokemon
    for pokemon in pokemon_list[:5]:
        print(pokemon.name)
        print(pokemon.types)
        print(pokemon.variations)
        print()
    
    pokemon_data = [pokemon.to_dict() for pokemon in pokemon_list]

    # Serialize to JSON and write to a file
    with open('pokemon_data.json', 'w', encoding='utf-8') as f:
        json.dump(pokemon_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
