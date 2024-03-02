import re, requests, json
from bs4 import BeautifulSoup
from pokemon import Pokemon, PokemonVariation
from pokemon import LEGENDARY_AND_MYTHICAL_POKEMON
from pokemon import TYPE_EFFECTIVENESS_CHART

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
        image_url = columns[0].find('img')['src']

        existing_pokemon = next((existing_pokemon for existing_pokemon in pokemon_list if existing_pokemon.id == pokedex_number), None)

        if existing_pokemon:
            variation = create_pokemon_variation(unparsed_name, types, image_url)
            existing_pokemon.add_variation(variation)
        else:
            pokemon = create_pokemon(pokedex_number, unparsed_name, types, image_url)
            pokemon_list.append(pokemon)

    return pokemon_list


def create_pokemon(pokedex_number, name, types, image_url):
    print(str(pokedex_number) + ". " + name)
    
    special_cases = {
        "Nidoran♀": "nidoran-f",
        "Nidoran♂": "nidoran-m",
        "Deoxys": "deoxys",
        "Burmy": "burmy",
        "Wormadam": "wormadam",
        "Giratina": "giratina",
        "Shaymin": "shaymin",
        "Basculin": "basculin",
        "Darmanitan": "darmanitan",
        "Tornadus": "tornadus",
        "Thundurus": "thundurus",
        "Landorus": "landorus",
        "Keldeo": "keldeo",
        "Meloetta": "meloetta",
        "Aegislash": "aegislash",
        "Pumpkaboo": "pumpkaboo",
        "Gourgeist": "gourgeist",
        "Zygarde": "zygarde",
        "Hoopa": "hoopa",
        "Oricorio": "oricorio",
        "Lycanroc": "lycanroc",
        "Wishiwashi": "wishiwashi",
        "Minior": "minior",
        "Toxtricity": "toxtricity",
        "Eiscue": "eiscue",
        "Indeedee": "indeedee",
        "Morpeko": "morpeko",
        "Zacian": "zacian",
        "Zamazenta": "zamazenta",
        "Urshifu": "urshifu",
        "Enamorus": "enamorus",
        "Farfetch'd": "farfetchd",
        "Sirfetch'd": "sirfetchd",
        "Mr. Mime": "mr-mime",
        "Mime Jr.": "mime-jr",
        "Mr. Rime": "mr-rime",
        "Flabébé": "flabebe",
        "Type: Null": "type-null",
        "Maushold": "maushold",
        "Squawkabilly": "squawkabilly",
        "Palafin": "palafin",
        "Tatsugiri": "tatsugiri",
        "Dudunsparce": "dudunsparce",
        "Gimmighoul": "gimmighoul",
        "Ogerpon": "ogerpon",
        "Terapagos": "terapagos",
        "Male": name.split(" Male")[0]
    }

    for case, url_name in special_cases.items():
        if case in name:
            if callable(url_name):
                url_name = url_name(name)
            print(name + ", " + str(url_name))
            response = requests.get(POKEMON_DETAILS_URL + url_name)
            break
    else:
        url_name = re.sub('[.:\' ]', '-', name)
        response = requests.get(POKEMON_DETAILS_URL + url_name)
        
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get pokemon height and weight
    vitals_table = soup.find('table', class_='vitals-table')
    height_row = vitals_table.find('th', string='Height')
    if height_row:
        height = height_row.find_next_sibling('td').string.strip().split('m')[0].strip()
    else:
        height = None

    weight_row = vitals_table.find('th', string='Weight')
    if weight_row:
        weight = weight_row.find_next_sibling('td').string.strip().split('kg')[0].strip()
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

    # Calculate type weaknesses, resistances, and immunities
    (resistances, weaknesses, immunities) = calculate_type_effectiveness(types)

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
        resistances=resistances,
        weaknesses=weaknesses,
        immunities=immunities,
        evolution_stage=evolution_stage,
        imageUrl=image_url,
        legendaryStatus=legendary_status
    )

    return pokemon


def get_moves_data(soup):
    moves_set = set()

    # Moves learnt by level up
    level_up_moves_table = soup.find('h3', string='Moves learnt by level up').find_next('table', class_='data-table')
    if level_up_moves_table:
        level_up_moves = [move.string.strip() for move in level_up_moves_table.find_all('a', class_='ent-name')]
        moves_set.update(level_up_moves)

    # Moves learnt by TM
    tm_moves_table = soup.find('h3', string='Moves learnt by TM').find_next('table', class_='data-table')
    if tm_moves_table:
        tm_moves = [move.string.strip() for move in tm_moves_table.find_all('a', class_='ent-name')]
        moves_set.update(tm_moves)
    
    # Egg moves
    egg_moves_table = soup.find('h3', string='Egg moves').find_next('table', class_='data-table')
    if egg_moves_table:
        egg_moves = [move.string.strip() for move in egg_moves_table.find_all('a', class_='ent-name')]
        moves_set.update(egg_moves)

    # Moves learnt on evolution
    evolution_moves_title = soup.find('h3', string='Moves learnt on evolution')
    if evolution_moves_title:
        evolution_moves_table = evolution_moves_title.find_next('table', class_='data-table') 
        evolution_moves = [move.string.strip() for move in evolution_moves_table.find_all('a', class_='ent-name')]
        moves_set.update(evolution_moves)

    # Moves learned by Tutor
    evolution_moves_title = soup.find('h3', string='Moves Tutor moves')
    if evolution_moves_title:
        evolution_moves_table = evolution_moves_title.find_next('table', class_='data-table')
        evolution_moves = [move.string.strip() for move in evolution_moves_table.find_all('a', class_='ent-name')]
        moves_set.update(evolution_moves)

    return list(moves_set)
    

def calculate_evolution_stage(soup, name):
    evolution_chart = soup.find('div', class_='infocard-list-evo')

    if evolution_chart:
        evolution_stages = evolution_chart.find_all('a', class_='ent-name')
        if evolution_stages:
            stage_counter = 1
            total_evolutions = len(evolution_stages)
            for evolution in evolution_stages:
                pokemon_name = evolution.string.strip()
                if pokemon_name == name:
                    return stage_counter, total_evolutions
                stage_counter += 1

    return None, None


def calculate_type_effectiveness(types):
    resistances = []
    weaknesses = []
    immunities = []

    for attacking_type in TYPE_EFFECTIVENESS_CHART:
        effectiveness = 1  # Default effectiveness
        for pokemon_type in types:
            effectiveness *= TYPE_EFFECTIVENESS_CHART[attacking_type].get(pokemon_type, 1)
        
        if effectiveness > 1:
            weaknesses.append(attacking_type)
        elif effectiveness < 1 and effectiveness > 0:
            resistances.append(attacking_type)
        elif effectiveness == 0:
            immunities.append(attacking_type)

    return resistances, weaknesses, immunities


def create_pokemon_variation(unparsed_name, types, image_url):
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
        variation_name = "Partner Pikachu"

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

    # Case for Hisuian
    elif "Hisuian" in unparsed_name:
        unparsed_variation_name = unparsed_name.split(" Hisuian ", 1)
        variation_name = 'Hisuian' + unparsed_variation_name[1]

    # Case for Rotom types: Heat, Wash, Frost, Fan, Mow
    elif "Rotom" in unparsed_name:
        variation_name = unparsed_name.split("Rotom", 1)[1].strip()
        
    # Case for Castform, Kyogre/Groudon, Deoxys, Burmy, Wormadam, Dialga/Palkia/Giratina, Shaymin, Tornadus, Thundurus, Landorous, Enamorous
    elif "Castform" or "Primal" or "Forme" or "Cloak" or "Keldeo" or "Calyrex" or "Palafin" or "Tatsugiri" or "Dudunsparce" or "Gimmighoul" or "Ogerpon" or "Terapagos" in unparsed_name:
        variation_name = unparsed_name
    
    # Calculate type weaknesses, resistances, and immunities
    (resistances, weaknesses, immunities) = calculate_type_effectiveness(types)
    
    variation = PokemonVariation(
        name=variation_name,
        types=types,
        resistances=resistances,
        weaknesses=weaknesses,
        immunities=immunities,
        imageUrl=image_url
    )

    return variation


def main():
    pokemon_list = scrape_pokemon_data()
    
    pokemon_data = [pokemon.to_dict() for pokemon in pokemon_list]

    # Serialize to JSON and write to a file
    with open('pokemon_data.json', 'w', encoding='utf-8') as f:
        json.dump(pokemon_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
