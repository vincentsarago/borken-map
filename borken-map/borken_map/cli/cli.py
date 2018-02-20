"""borken_map.cli.cli"""

import os
import uuid
import click
import cligj

from supermercado import super_utils
from borken_map.utils import create_img


@click.command()
@click.option('--min-zoom', type=int, default=8, help='')
@click.option('--max-zoom', type=int, default=13, help='')
@click.option('--mapid', type=str, default='mapbox.satellite')
@click.option('--col', type=int, default=3, help='')
@click.option('--row', type=int, default=3, help='')
@cligj.features_in_arg
def create(features, min_zoom, max_zoom, mapid, col, row):
    """
    """
    access_token = os.environ['MapboxAccessToken']
    features = [f for f in super_utils.filter_polygons(features)]
    img = create_img(features, access_token, min_zoom, max_zoom, mapid, nb_col=col, nb_row=row)
    renderid = str(uuid.uuid1())
    outfile = f'./{renderid}.jpg'
    img.save(outfile)
