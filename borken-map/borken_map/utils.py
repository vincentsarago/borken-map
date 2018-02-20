"""borken_map.utils"""

import os
from io import BytesIO
from concurrent import futures

import requests
from PIL import Image

from random import randint
from supermercado.burntiles import burn


def create_img(features, access_token, min_zoom=6, max_zoom=13, mapid='mapbox.satellite', nb_col=14, nb_row=10):
    """
    """

    img_size_x = nb_col * 512
    img_size_y = nb_row * 512
    new_im = Image.new('RGB', (img_size_x, img_size_y))

    ind = []
    for i in range(0, img_size_x, 512):
        for j in range(0, img_size_y, 512):
            ind.append({'c': i, 'r': j})

    def worker(idx):
        """
        """
        nb_features = len(features)
        while True:
            zoom = randint(min_zoom, max_zoom)
            feature = features[randint(0, nb_features - 1)]

            tiles = burn([feature], zoom)
            nb_mctiles = len(tiles)
            tile = tiles[randint(0, nb_mctiles - 1)]
            tile_x = tile[0]
            tile_y = tile[1]
            tile_z = tile[2]

            url = f'https://api.mapbox.com/v4/{mapid}/{tile_z}/{tile_x}/{tile_y}@2x.jpg?access_token={access_token}'
            response = requests.get(url)
            if response.status_code != 200:
                continue

            header = response.headers
            size = header.get('Content-Length')
            if int(size) < 10000:
                continue

            new_im.paste(Image.open(BytesIO(response.content)), (idx['c'], idx['r']))
            return True

    with futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(worker, ind)

    new_im = new_im.convert('RGBA')

    imageWatermark = Image.new('RGBA', new_im.size, (255, 255, 255, 0))
    img_logo = os.path.join(os.path.dirname(__file__), 'data', 'mapbox.png')
    logo = Image.open(img_logo)
    imageWatermark.paste(logo, (20, img_size_y - 80))
    new_im = Image.alpha_composite(new_im, imageWatermark).convert('RGB')

    if mapid == 'mapbox.satellite':
        img_logo = os.path.join(os.path.dirname(__file__), 'data', 'mb_dg.png')
        logo = Image.open(img_logo).convert('RGB')
        h = logo.height
        w = logo.width
        new_im.paste(logo, (img_size_x - w, img_size_y - h))
    else:
        img_logo = os.path.join(os.path.dirname(__file__), 'data', 'mb_osm.png')
        logo = Image.open(img_logo).convert('RGB')
        h = logo.height
        w = logo.width
        new_im.paste(logo, (img_size_x - w, img_size_y - h))

    return new_im
