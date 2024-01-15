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
            # print("pokemon: " + existing_pokemon.name)
            existing_pokemon.add_variation(variation)
        else:
            pokemon = create_pokemon(pokedex_number, unparsed_name, types)
            pokemon_list.append(pokemon)

    return pokemon_list


def create_pokemon(pokedex_number, name, types):
    print(str(pokedex_number) + ". " + name)
    if "Nidoran" in name:
        if "♀" in name:
            response = requests.get(POKEMON_DETAILS_URL + "nidoran-f")
        else:
            response = requests.get(POKEMON_DETAILS_URL + "nidoran-m")
    elif "Male" in name:
        response = requests.get(POKEMON_DETAILS_URL + name.split()[0])
    elif "'" in name:
        response = requests.get(POKEMON_DETAILS_URL + name.replace("'", ""))
    elif "." in name:
        response = requests.get(POKEMON_DETAILS_URL + name.replace(".", "").replace(" ", "-"))
    elif ":" in name:
        response = requests.get(POKEMON_DETAILS_URL + name.replace(":", "").replace(" ", "-"))
    elif "é" in name:
        response = requests.get(POKEMON_DETAILS_URL + name.replace("é", "e"))
    elif "Deoxys" in name:
        response = requests.get(POKEMON_DETAILS_URL + "deoxys")
    elif "Burmy" in name:
        response = requests.get(POKEMON_DETAILS_URL + "burmy")
    elif "Wormadam" in name:
        response = requests.get(POKEMON_DETAILS_URL + "wormadam")
    elif "Giratina" in name:
        response = requests.get(POKEMON_DETAILS_URL + "giratina")
    elif "Shaymin" in name:
        response = requests.get(POKEMON_DETAILS_URL + "shaymin")
    elif "Basculin" in name:
        response = requests.get(POKEMON_DETAILS_URL + "basculin")
    elif "Darmanitan" in name:
        response = requests.get(POKEMON_DETAILS_URL + "darmanitan")
    elif "Tornadus" in name:
        response = requests.get(POKEMON_DETAILS_URL + "tornadus")
    elif "Thundurus" in name:
        response = requests.get(POKEMON_DETAILS_URL + "thundurus")
    elif "Landorus" in name:
        response = requests.get(POKEMON_DETAILS_URL + "landorus")
    elif "Keldeo" in name:
        response = requests.get(POKEMON_DETAILS_URL + "keldeo")
    elif "Meloetta" in name:
        response = requests.get(POKEMON_DETAILS_URL + "meloetta")
    elif "Aegislash" in name:
        response = requests.get(POKEMON_DETAILS_URL + "aegislash")
    elif "Pumpkaboo" in name:
        response = requests.get(POKEMON_DETAILS_URL + "pumpkaboo")
    elif "Gourgeist" in name:
        response = requests.get(POKEMON_DETAILS_URL + "gourgeist")
    elif "Zygarde" in name:
        response = requests.get(POKEMON_DETAILS_URL + "zygarde")
    elif "Hoopa" in name:
        response = requests.get(POKEMON_DETAILS_URL + "hoopa")
    elif "Oricorio" in name:
        response = requests.get(POKEMON_DETAILS_URL + "oricorio")
    elif "Lycanroc" in name:
        response = requests.get(POKEMON_DETAILS_URL + "lycanroc")
    elif "Wishiwashi" in name:
        response = requests.get(POKEMON_DETAILS_URL + "wishiwashi")
    elif "Minior" in name:
        response = requests.get(POKEMON_DETAILS_URL + "minior")
    elif "Toxtricity" in name:
        response = requests.get(POKEMON_DETAILS_URL + "toxtricity")
    elif "Eiscue" in name:
        response = requests.get(POKEMON_DETAILS_URL + "eiscue")
    elif "Morpeko" in name:
        response = requests.get(POKEMON_DETAILS_URL + "morpeko")
    elif "Zacian" in name:
        response = requests.get(POKEMON_DETAILS_URL + "zacian")
    elif "Zamazenta" in name:
        response = requests.get(POKEMON_DETAILS_URL + "zamazenta")
    elif "Urshifu" in name:
        response = requests.get(POKEMON_DETAILS_URL + "urshifu")
    elif "Enamorus" in name:
        response = requests.get(POKEMON_DETAILS_URL + "enamorus")
    elif "Meowstic" in name:
        response = requests.get(POKEMON_DETAILS_URL + "meowstic")
    elif "Family" in name:
        response = requests.get(POKEMON_DETAILS_URL + "Maushold")
    elif "Plumage" in name:
        response = requests.get(POKEMON_DETAILS_URL + "squawkabilly")
    elif "Palafin" in name:
        response = requests.get(POKEMON_DETAILS_URL + "palafin")
    elif "Tatsugiri" in name:
        response = requests.get(POKEMON_DETAILS_URL + "tatsugiri")
    elif "Dudunsparce" in name:
        response = requests.get(POKEMON_DETAILS_URL + "dudunsparce")
    elif "Gimmighoul" in name:
        response = requests.get(POKEMON_DETAILS_URL + "gimmighoul")
    elif "Ogerpon" in name:
        response = requests.get(POKEMON_DETAILS_URL + "ogerpon")
    elif "Terapagos" in name:
        response = requests.get(POKEMON_DETAILS_URL + "terapagos")
    elif " " in name:
        response = requests.get(POKEMON_DETAILS_URL + name.replace(" ", "-"))
    else:
        response = requests.get(POKEMON_DETAILS_URL + name)
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get pokemon image url
    if "Nidoran" in name:
        if "♀" in name:
            image_url = "https://img.pokemondb.net/artwork/nidoran-f.jpg"
        else:
            image_url = "https://img.pokemondb.net/artwork/nidoran-m.jpg"
    elif "Male" in name:
        name_split = name.split()
        data_title = f"{name_split[0]}-{name_split[1]}"
        a_tag = soup.find("a", {"data-title": data_title})
        if a_tag:
            image_url = image.find('img')['src']
        else:
            image_url = None
    elif "Deoxys" in name:
        image_url = "https://img.pokemondb.net/artwork/deoxys-normal.jpg"
    elif "Burmy" in name:
        image_url = "https://img.pokemondb.net/artwork/burmy-plant.jpg"
    elif "Wormadam" in name:
        image_url = "https://img.pokemondb.net/artwork/wormadam-plant.jpg"
    elif "Giratina" in name:
        image_url = "https://img.pokemondb.net/artwork/giratina-altered.jpg"
    elif "Shaymin" in name:
        image_url = "https://img.pokemondb.net/artwork/shaymin-land.jpg"
    elif "Basculin" in name:
        image_url = "https://img.pokemondb.net/artwork/basculin-blue-striped.jpg"
    elif "Darmanitan" in name:
        image_url = "https://img.pokemondb.net/artwork/darmanitan-standard.jpg"
    elif "Tornadus" in name:
        image_url = "https://img.pokemondb.net/artwork/tornadus-incarnate.jpg"
    elif "Thundurus" in name:
        image_url = "https://img.pokemondb.net/artwork/thundurus-incarnate.jpg"
    elif "Landorus" in name:
        image_url = "https://img.pokemondb.net/artwork/landorus-incarnate.jpg"
    elif "Keldeo" in name:
        image_url = "https://img.pokemondb.net/artwork/keldeo-ordinary.jpg"
    elif "Meloetta" in name:
        image_url = "https://img.pokemondb.net/artwork/meloetta-aria.jpg"
    elif "Aegislash" in name:
        image_url = "https://img.pokemondb.net/artwork/aegislash-shield.jpg"
    elif "Pumpkaboo" in name:
        image_url = "https://img.pokemondb.net/artwork/pumpkaboo-average.jpg"
    elif "Gourgeist" in name:
        image_url = "https://img.pokemondb.net/artwork/gourgeist-average.jpg"
    elif "Zygarde" in name:
        image_url = "https://img.pokemondb.net/artwork/zygarde-50.jpg"
    elif "Hoopa" in name:
        image_url = "https://img.pokemondb.net/artwork/hoopa-confined.jpg"
    elif "Oricorio" in name:
        image_url = "https://img.pokemondb.net/artwork/oricorio-baile.jpg"
    elif "Lycanroc" in name:
        image_url = "https://img.pokemondb.net/artwork/lycanroc-midday.jpg"
    elif "Wishiwashi" in name:
        image_url = "https://img.pokemondb.net/artwork/wishiwashi-solo.jpg"
    elif "Minior" in name:
        image_url = "https://img.pokemondb.net/artwork/minior-red-meteor.jpg"
    elif "Toxtricity" in name:
        image_url = "https://img.pokemondb.net/artwork/toxtricity-amped.jpg"
    elif "Eiscue" in name:
        image_url = "https://img.pokemondb.net/artwork/eiscue-ice.jpg"
    elif "Indeedee" in name:
        image_url = "https://img.pokemondb.net/artwork/indeedee-male.jpg"
    elif "Morpeko" in name:
        image_url = "https://img.pokemondb.net/artwork/morpeko-full-belly.jpg"
    elif "Zacian" in name:
        image_url = "https://img.pokemondb.net/artwork/zacian-hero.jpg"
    elif "Zamazenta" in name:
        image_url = "https://img.pokemondb.net/artwork/zamazenta-hero.jpg"
    elif "Urshifu" in name:
        image_url = "https://img.pokemondb.net/artwork/urshifu-single-strike.jpg"
    elif "Enamorus" in name:
        image_url = "https://img.pokemondb.net/artwork/enamorus-incarnate.jpg"
    elif "é" in name:
        image_url = "https://img.pokemondb.net/artwork/flabebe.jpg"
    elif "Meowstic" in name:
        image_url = "https://img.pokemondb.net/artwork/meowstic-male.jpg"
    elif "Family" in name:
        image_url = "https://img.pokemondb.net/artwork/maushold.jpg"
    elif "Plumage" in name:
        image_url = "https://img.pokemondb.net/artwork/squawkabilly.jpg"
    elif "Palafin" in name:
        image_url = "https://img.pokemondb.net/artwork/palafin.jpg"
    elif "Tatsugiri" in name:
        image_url = "https://img.pokemondb.net/artwork/tatsugiri.jpg"
    elif "Dudunsparce" in name:
        image_url = "https://img.pokemondb.net/artwork/dudunsparce.jpg"
    elif "Gimmighoul" in name:
        image_url = "https://img.pokemondb.net/artwork/gimmighoul.jpg"
    elif "Ogerpon" in name:
        image_url = "https://img.pokemondb.net/artwork/ogerpon.jpg"
    elif "Terapagos" in name:
        image_url = "https://img.pokemondb.net/artwork/terapagos.jpg"
    elif "Sinistcha" in name:
        image_url = "https://img.pokemondb.net/artwork/sinistcha.jpg"
    elif "Hydrapple" in name:
        image_url = "https://img.pokemondb.net/artwork/hydrapple.jpg"
    elif "Gouging Fire" in name:
        image_url = "https://img.pokemondb.net/artwork/gouging-fire.jpg"
    elif "Iron Boulder" in name:
        image_url = "https://img.pokemondb.net/artwork/iron-boulder.jpg"
    elif "Iron Crown" in name:
        image_url = "https://img.pokemondb.net/artwork/iron-crown.jpg"
    else:
        image = soup.find('a', attrs={'data-title': f'{name} official artwork'})
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

    # Calculate type weaknesses, strengths, and immunities
    # (strengths, weaknesses, immunities) = calculate_type_advantages(types)
    

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
        strengths=[],
        weaknesses=[],
        immunities=[],
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
    

    
    variation = PokemonVariation(
        name=variation_name,
        types=types,
        strengths=[],
        weaknesses=[],
        immunities=[],
        imageUrl=""
    )

    return variation


def main():
    pokemon_list = scrape_pokemon_data()

    # Print the first 5 pokemon
    for pokemon in pokemon_list[:6]:
        print(pokemon.name)
        print(pokemon.types)
        print(pokemon.variations)
        print()
    
    # pokemon_data = [pokemon.to_dict() for pokemon in pokemon_list]
    pokemon_data = []
    for pokemon in pokemon_list:
        print("pokemon: " + pokemon.name)
        if pokemon.variations is None:
            pokemon.variations = []
        else: 
            for variation in pokemon.variations:
                print("variation: " + variation.name)
        pokemon_data.append(pokemon.to_dict())

    # Serialize to JSON and write to a file
    with open('pokemon_data.json', 'w', encoding='utf-8') as f:
        json.dump(pokemon_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
