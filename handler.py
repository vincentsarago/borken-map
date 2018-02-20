"""borken_map.handler"""

import os
import json
import uuid
from io import BytesIO
from random import randint

import boto3
import tweepy
from PIL import Image
from borken_map.utils import create_img


def handler(event, context):
    """Tweet the image
    """
    consumer_key = os.environ['C_KEY']
    consumer_secret = os.environ['C_SECRET']
    access_key = os.environ['A_KEY']
    access_secret = os.environ['A_SECRET']
    access_token = os.environ['MapboxAccessToken']
    out_bucket = os.environ['OUTPUT_BUCKET']

    min_zoom = event.get('min_zoom', 8)
    max_zoom = event.get('max_zoom', 13)
    mapid = event.get('mapid')
    col = event.get('col', 6)
    row = event.get('row', 4)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    feat = os.path.join(os.path.dirname(__file__), 'data', 'world.geojson')
    with open(feat, 'r') as f:
        feats = json.loads(f.read())['features']

    if not mapid:
        mapids = [
            'mapbox.streets',
            'mapbox.light',
            'mapbox.satellite',
            'mapbox.wheatpaste',
            'mapbox.streets-basic',
            'mapbox.comic',
            'mapbox.outdoors',
            'mapbox.run-bike-hike',
            'mapbox.pencil',
            'mapbox.pirates',
            'mapbox.emerald',
            'mapbox.high-contrast']
        mapid = mapids[randint(0, len(mapids) - 1)]

    img = create_img(feats, access_token, min_zoom=min_zoom, max_zoom=max_zoom,
                     mapid=mapid, nb_col=col, nb_row=row)

    # Upload high res to s3
    uid = str(uuid.uuid1())
    key = f'data/borken_map/{uid}.jpg'
    params = {
        'ACL': 'public-read',
        'ContentType': 'image/jpeg'}

    im = BytesIO()
    img.save(im, 'jpeg', subsampling=0, quality=100)
    im.seek(0)

    client = boto3.client('s3')
    client.put_object(Body=im, Bucket=out_bucket, Key=key, **params)

    # Create a thumbnail
    img.thumbnail((1024, 1024), Image.ANTIALIAS)

    im = BytesIO()
    img.save(im, 'jpeg', subsampling=0, quality=100)
    im.seek(0)

    tweet_content = f'Download full resolution at https://s3.amazonaws.com/{out_bucket}/{key} #maptiles'
    api.update_with_media('borken_map.jpg', status=tweet_content, file=im)
    return True
