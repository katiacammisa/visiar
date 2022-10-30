import pandas as pd


class Pokemon:
    def __init__(self, number, name, attack, baseExp, type, category, weight, height, abilities, image):
        self.number = number
        self.name = name
        self.attack = attack
        self.baseExp = baseExp
        self.type = type
        self.category = category
        self.weight = weight
        self.height = height
        self.abilities = abilities
        self.image = image


def getPokemonData():
    df = pd.read_csv('PokemonData.csv')
    df = df.sort_values(by=['#'], ascending=True)
    df = df[['#', 'Abilities', 'Attack', 'Base EXP', 'Egg Groups', 'Height', 'Name', 'Type', 'Weight', 'Image']]
    df = df.drop_duplicates(subset=["#"], ignore_index=True)
    pokeDict = {}
    for poke in range(1, 152):
        pokeDict[poke] = Pokemon(df.get('#')[poke], df.get('Name')[poke], df.get('Attack')[poke],
                                 df.get('Base EXP')[poke],
                                 df.get('Type')[poke], df.get('Egg Groups')[poke], df.get('Weight')[poke],
                                 df.get('Height')[poke], df.get('Abilities')[poke], df.get('Image')[poke])
    return pokeDict


getPokemonData()
