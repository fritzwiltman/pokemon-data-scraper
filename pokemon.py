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
    def __init__(self, name, types, strengths, weaknesses, immunities, imageUrl):
        self.name = name
        self.types = types
        self.strengths = strengths
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.imageUrl = imageUrl

    def to_dict(self):
        return {
            'name': self.name,
            'types': self.types,
            'strengths': self.strengths,
            'weaknesses': self.weaknesses,
            'immunities': self.immunities,
            'imageUrl': self.imageUrl
        }

class Pokemon:
    def __init__(self, id, name, types, height, weight, category, abilities, moves, strengths, weaknesses, immunities, evolution_stage, imageUrl, legendaryStatus):
        self.id = id
        self.name = name
        self.types = types
        self.height = height
        self.weight = weight
        self.category = category
        self.abilities = abilities
        self.moves = moves
        self.strengths = strengths
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
            'strengths': self.strengths,
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

# Usage Example
charizard = Pokemon(
    id=6,
    name="Charizard",
    types=["Fire", "Flying"],
    height="1.7 m",
    weight="90.5 kg",
    category="Flame Pokémon",
    abilities=["Blaze"],
    evolution_stage=(3,3),
    moves=["Flamethrower", "Fire Blast", "Fly", "Cut"],
    strengths=["Grass", "Bug", "Steel", "Fire", "Fairy", "Fighting"],
    weaknesses=["Water", "Electric", "Rock"],
    immunities=[],
    imageUrl="https://example.com/charizard.png",
    legendaryStatus=False
)

mega_charizard_x = PokemonVariation(
    name="Mega Charizard X",
    types=["Fire", "Dragon"],
    strengths=["Water", "Electric", "Rock", "Steel"],
    weaknesses=["Ground", "Rock", "Dragon"],
    immunities=["Electric"],
    imageUrl="https://example.com/mega_charizard_x.png"
)

charizard.add_variation(mega_charizard_x)
