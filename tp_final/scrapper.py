import requests


def saveImageFromUrl(n, url):
    img_data = requests.get(url).content
    with open(f'./images/{n}.png', 'wb') as handler:
        handler.write(img_data)
