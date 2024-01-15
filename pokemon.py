"""
class Stats:
    def __init__(self, hp, attack, defense, specialAttack, specialDefense, speed):
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.specialAttack = specialAttack
        self.specialDefense = specialDefense
        self.speed = speed
"""

class PokemonVariation:
    def __init__(self, name, types, resistances, weaknesses, immunities, imageUrl):
        self.name = name
        self.types = types
        self.resistances = resistances
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.imageUrl = imageUrl

    def to_dict(self):
        return {
            'name': self.name,
            'types': self.types,
            'resistances': self.resistances,
            'weaknesses': self.weaknesses,
            'immunities': self.immunities,
            'imageUrl': self.imageUrl
        }

class Pokemon:
    def __init__(self, id, name, types, height, weight, category, abilities, moves, resistances, weaknesses, immunities, evolution_stage, imageUrl, legendaryStatus):
        self.id = id
        self.name = name
        self.types = types
        self.height = height
        self.weight = weight
        self.category = category
        self.abilities = abilities
        self.moves = moves
        self.resistances = resistances
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.evolution_stage = evolution_stage # 1, 2, 3, or None to denote no evolution
        self.imageUrl = imageUrl
        self.legendaryStatus = legendaryStatus
        self.variations = []

    def add_variation(self, variation):
        self.variations.append(variation)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'types': self.types,
            'height': self.height,
            'weight': self.weight,
            'category': self.category,
            'abilities': self.abilities,
            'moves': self.moves,
            'resistances': self.resistances,
            'weaknesses': self.weaknesses,
            'immunities': self.immunities,
            'evolutionStage': self.evolution_stage,
            'imageUrl': self.imageUrl,
            'legendaryStatus': self.legendaryStatus,
            'variations': [variation.to_dict() for variation in self.variations]
        }

LEGENDARY_AND_MYTHICAL_POKEMON = [
     "Articuno", "Zapdos", "Moltres",
    "Mewtwo",
    "Raikou", "Entei", "Suicune",
    "Lugia", "Ho-Oh",
    "Regirock", "Regice", "Registeel",
    "Latias", "Latios",
    "Kyogre", "Groudon", "Rayquaza",
    "Uxie", "Mesprit", "Azelf",
    "Dialga", "Palkia", "Giratina",
    "Heatran", "Regigigas",
    "Cresselia",
    "Cobalion", "Terrakion", "Virizion", "Keldeo",
    "Tornadus", "Thundurus", "Landorus",
    "Reshiram", "Zekrom", "Kyurem",
    "Xerneas", "Yveltal", "Zygarde",
    "Tapu Koko", "Tapu Lele", "Tapu Bulu", "Tapu Fini",
    "Solgaleo", "Lunala",
    "Nihilego", "Buzzwole", "Pheromosa", "Xurkitree", "Celesteela", "Kartana", "Guzzlord",
    "Necrozma",
    "Zacian", "Zamazenta",
    "Eternatus",
    "Mew",
    "Celebi",
    "Jirachi",
    "Deoxys",
    "Darkrai",
    "Shaymin",
    "Arceus",
    "Victini",
    "Keldeo",
    "Meloetta",
    "Genesect",
    "Diancie",
    "Hoopa",
    "Volcanion",
    "Magearna",
    "Marshadow",
    "Zeraora",
    "Meltan", "Melmetal",
    "Zarude"
]


TYPE_EFFECTIVENESS_CHART = {
    'Normal': {'Rock': 0.5, 'Ghost': 0, 'Steel': 0.5},
    'Fire': {'Fire': 0.5, 'Water': 0.5, 'Grass': 2, 'Ice': 2, 'Bug': 2, 'Rock': 0.5, 'Dragon': 0.5, 'Steel': 2},
    'Water': {'Fire': 2, 'Water': 0.5, 'Grass': 0.5, 'Ground': 2, 'Rock': 2, 'Dragon': 0.5},
    'Electric': {'Water': 2, 'Electric': 0.5, 'Grass': 0.5, 'Ground': 0, 'Flying': 2, 'Dragon': 0.5},
    'Grass': {'Fire': 0.5, 'Water': 2, 'Grass': 0.5, 'Poison': 0.5, 'Ground': 2, 'Flying': 0.5, 'Bug': 0.5, 'Rock': 2, 'Dragon': 0.5, 'Steel': 0.5},
    'Ice': {'Fire': 0.5, 'Water': 0.5, 'Grass': 2, 'Ice': 0.5, 'Ground': 2, 'Flying': 2, 'Dragon': 2, 'Steel': 0.5},
    'Fighting': {'Normal': 2, 'Ice': 2, 'Poison': 0.5, 'Flying': 0.5, 'Psychic': 0.5, 'Bug': 0.5, 'Rock': 2, 'Ghost': 0, 'Dark': 2, 'Steel': 2, 'Fairy': 0.5},
    'Poison': {'Grass': 2, 'Poison': 0.5, 'Ground': 0.5, 'Rock': 0.5, 'Ghost': 0.5, 'Steel': 0, 'Fairy': 2},
    'Ground': {'Fire': 2, 'Electric': 2, 'Grass': 0.5, 'Poison': 2, 'Flying': 0, 'Bug': 0.5, 'Rock': 2, 'Steel': 2},
    'Flying': {'Electric': 0.5, 'Grass': 2, 'Fighting': 2, 'Bug': 2, 'Rock': 0.5, 'Steel': 0.5},
    'Psychic': {'Fighting': 2, 'Poison': 2, 'Psychic': 0.5, 'Dark': 0, 'Steel': 0.5},
    'Bug': {'Fire': 0.5, 'Grass': 2, 'Fighting': 0.5, 'Poison': 0.5, 'Flying': 0.5, 'Psychic': 2, 'Ghost': 0.5, 'Dark': 2, 'Steel': 0.5, 'Fairy': 0.5},
    'Rock': {'Fire': 2, 'Ice': 2, 'Fighting': 0.5, 'Ground': 0.5, 'Flying': 2, 'Bug': 2, 'Steel': 0.5},
    'Ghost': {'Normal': 0, 'Psychic': 2, 'Ghost': 2, 'Dark': 0.5},
    'Dragon': {'Dragon': 2, 'Steel': 0.5, 'Fairy': 0},
    'Dark': {'Fighting': 0.5, 'Psychic': 2, 'Ghost': 2, 'Dark': 0.5, 'Fairy': 0.5},
    'Steel': {'Fire': 0.5, 'Water': 0.5, 'Electric': 0.5, 'Ice': 2, 'Rock': 2, 'Steel': 0.5, 'Fairy': 2},
    'Fairy': {'Fire': 0.5, 'Fighting': 2, 'Poison': 0.5, 'Dragon': 2, 'Dark': 2, 'Steel': 0.5}   
}
