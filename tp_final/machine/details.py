import pandas as pd


class Pokemon:
    def __init__(self, number, name, type1, total, hp, attack, defense, spAttack, spDefence, speed, legendary):
        self.number = number
        self.name = name
        self.type1 = type1
        self.total = total
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.spAttack = spAttack
        self.spDefence = spDefence
        self.speed = speed
        self.legendary = legendary


def getPokemonData():
    df = pd.read_csv('PokemonData.csv')
    df = df.sort_values(by=['#'], ascending=True)
    df = df[['#', 'Name', 'Type 1', 'Total', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Legendary']]
    pokeDict = {}
    for poke in range(150):
        pokeDict[poke] = Pokemon(df.get('#')[poke], df.get('Name')[poke], df.get('Type 1')[poke],
                                 df.get('Total')[poke],
                                 df.get('HP')[poke], df.get('Attack')[poke], df.get('Defense')[poke],
                                 df.get('Sp. Atk')[poke], df.get('Sp. Def')[poke], df.get('Speed')[poke],
                                 df.get('Legendary')[poke])
    return pokeDict


getPokemonData()
