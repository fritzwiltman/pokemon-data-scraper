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

        existing_pokemon = next((existing_pokemon for existing_pokemon in pokemon_list if existing_pokemon.id == pokedex_number), None)

        if existing_pokemon:
            variation = create_pokemon_variation(unparsed_name, types)
            # print("pokemon: " + existing_pokemon.name)
            existing_pokemon.add_variation(variation)
        else:
            pokemon = create_pokemon(pokedex_number, unparsed_name, types)
            pokemon_list.append(pokemon)

    return pokemon_list


def create_pokemon(pokedex_number, name, types):
    print(str(pokedex_number) + ". " + name)

    special_cases = {
        "Nidoran♀": ("nidoran-f", "https://img.pokemondb.net/artwork/nidoran-f.jpg"),
        "Nidoran♂": ("nidoran-m", "https://img.pokemondb.net/artwork/nidoran-m.jpg"),
        "Deoxys": ("deoxys", "https://img.pokemondb.net/artwork/deoxys-normal.jpg"),
        "Burmy": ("burmy", "https://img.pokemondb.net/artwork/burmy-plant.jpg"),
        "Wormadam": ("wormadam", "https://img.pokemondb.net/artwork/wormadam-plant.jpg"),
        "Giratina": ("giratina", "https://img.pokemondb.net/artwork/giratina-altered.jpg"),
        "Shaymin": ("shaymin", "https://img.pokemondb.net/artwork/shaymin-land.jpg"),
        "Basculin": ("basculin", "https://img.pokemondb.net/artwork/basculin-blue-striped.jpg"),
        "Darmanitan": ("darmanitan", "https://img.pokemondb.net/artwork/darmanitan-standard.jpg"),
        "Tornadus": ("tornadus", "https://img.pokemondb.net/artwork/tornadus-incarnate.jpg"),
        "Thundurus": ("thundurus", "https://img.pokemondb.net/artwork/thundurus-incarnate.jpg"),
        "Landorus": ("landorus", "https://img.pokemondb.net/artwork/landorus-incarnate.jpg"),
        "Keldeo": ("keldeo", "https://img.pokemondb.net/artwork/keldeo-ordinary.jpg"),
        "Meloetta": ("meloetta", "https://img.pokemondb.net/artwork/meloetta-aria.jpg"),
        "Aegislash": ("aegislash", "https://img.pokemondb.net/artwork/aegislash-shield.jpg"),
        "Pumpkaboo": ("pumpkaboo", "https://img.pokemondb.net/artwork/pumpkaboo-average.jpg"),
        "Gourgeist": ("gourgeist", "https://img.pokemondb.net/artwork/gourgeist-average.jpg"),
        "Zygarde": ("zygarde", "https://img.pokemondb.net/artwork/zygarde-50.jpg"),
        "Hoopa": ("hoopa", "https://img.pokemondb.net/artwork/hoopa-confined.jpg"),
        "Oricorio": ("oricorio", "https://img.pokemondb.net/artwork/oricorio-baile.jpg"),
        "Lycanroc": ("lycanroc", "https://img.pokemondb.net/artwork/lycanroc-midday.jpg"),
        "Wishiwashi": ("wishiwashi", "https://img.pokemondb.net/artwork/wishiwashi-solo.jpg"),
        "Minior": ("minior", "https://img.pokemondb.net/artwork/minior-red-meteor.jpg"),
        "Toxtricity": ("toxtricity", "https://img.pokemondb.net/artwork/toxtricity-amped.jpg"),
        "Eiscue": ("eiscue", "https://img.pokemondb.net/artwork/eiscue-ice.jpg"),
        "Indeedee": ("indeedee", "https://img.pokemondb.net/artwork/indeedee-male.jpg"),
        "Morpeko": ("morpeko", "https://img.pokemondb.net/artwork/morpeko-full-belly.jpg"),
        "Zacian": ("zacian", "https://img.pokemondb.net/artwork/zacian-hero.jpg"),
        "Zamazenta": ("zamazenta", "https://img.pokemondb.net/artwork/zamazenta-hero.jpg"),
        "Urshifu": ("urshifu", "https://img.pokemondb.net/artwork/urshifu-single-strike.jpg"),
        "Enamorus": ("enamorus", "https://img.pokemondb.net/artwork/enamorus-incarnate.jpg"),
        "Farfetch'd": ("farfetchd", "https://img.pokemondb.net/artwork/farfetchd.jpg"),
        "Sirfetch'd": ("sirfetchd", "https://img.pokemondb.net/artwork/sirfetchd.jpg"),
        "Mr. Mime": ("mr-mime", "https://img.pokemondb.net/artwork/mr-mime.jpg"),
        "Mime Jr.": ("mime-jr", "https://img.pokemondb.net/artwork/mime-jr.jpg"),
        "Mr. Rime": ("mr-rime", "https://img.pokemondb.net/artwork/mr-rime.jpg"),
        "Flabébé": ("flabebe", "https://img.pokemondb.net/artwork/flabebe.jpg"),
        "Type: Null": ("type-null", "https://img.pokemondb.net/artwork/type-null.jpg"),
        "Maushold": ("maushold", "https://img.pokemondb.net/artwork/maushold.jpg"),
        "Squawkabilly": ("squawkabilly", "https://img.pokemondb.net/artwork/squawkabilly.jpg"),
        "Palafin": ("palafin", "https://img.pokemondb.net/artwork/palafin.jpg"),
        "Tatsugiri": ("tatsugiri", "https://img.pokemondb.net/artwork/tatsugiri.jpg"),
        "Dudunsparce": ("dudunsparce", "https://img.pokemondb.net/artwork/dudunsparce.jpg"),
        "Gimmighoul": ("gimmighoul", "https://img.pokemondb.net/artwork/gimmighoul.jpg"),
        "Ogerpon": ("ogerpon", "https://img.pokemondb.net/artwork/ogerpon.jpg"),
        "Terapagos": ("terapagos", "https://img.pokemondb.net/artwork/terapagos.jpg"),
        "Male": (name.split(" Male")[0], None)
    }

    for case, (url_name, image_url) in special_cases.items():
        if case in name:
            if callable(url_name):
                url_name = url_name(name)
            response = requests.get(POKEMON_DETAILS_URL + url_name)
            break
    else:
        url_name = re.sub('[.:\' ]', '-', name)
        response = requests.get(POKEMON_DETAILS_URL + url_name)

    soup = BeautifulSoup(response.text, 'html.parser')

    for case, (url_name, image_url) in special_cases.items():
        if case in name:
            image_url = image_url
            break

    if image_url is None:
        image = soup.find('a', attrs={'data-title': f'{name} official artwork'})
        if image:
            image_url = image.find('img')['src']

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
        imageUrl=""
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
