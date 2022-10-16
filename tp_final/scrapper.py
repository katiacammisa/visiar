import requests


def scrapPokemons():
    for n in range(1, 10):
        img_data = requests.get(f'https://assets.pokemon.com/assets/cms2/img/pokedex/detail/00{n}.png').content
        with open(f'./images/{n}.png', 'wb') as handler:
            handler.write(img_data)

    for n in range(11, 100):
        img_data = requests.get(f'https://assets.pokemon.com/assets/cms2/img/pokedex/detail/0{n}.png').content
        with open(f'./images/{n}.png', 'wb') as handler:
            handler.write(img_data)

    for n in range(100, 152):
        img_data = requests.get(f'https://assets.pokemon.com/assets/cms2/img/pokedex/detail/{n}.png').content
        with open(f'./images/{n}.png', 'wb') as handler:
            handler.write(img_data)


# scrapPokemons()


def getFromUrl(n,url):
    img_data = requests.get(url).content
    with open(f'./images/{n}.png', 'wb') as handler:
        handler.write(img_data)
