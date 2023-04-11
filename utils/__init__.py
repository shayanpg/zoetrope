import boto3
from botocore.exceptions import ClientError
import logging
import os
import streetview
import urllib
from ast import literal_eval
import math
import re, random
from shapely.geometry import Polygon, Point

from gsv import settings
from pull.models import Pull
from image.models import Image
from datetime import datetime

DOWNLOAD_DIR = './downloads/'

MONTH_MAP = {
    1:"January",
    2:"February",
    3:"March",
    4:"April",
    5:"May",
    6:"June",
    7:"July",
    8:"August",
    9:"September",
    10:"October",
    11:"November",
    12:"December",
}

def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees, (roation from A to B)
    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

def geocode_address(address, m_key):
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = "?address=%s&key=%s" % (address.replace(' ', '+'), m_key)
    add_json = urllib.request.urlopen(base_url+params).read()
    data = literal_eval(add_json.decode('utf8'))
    if not data.get('results') or data.get('status') == "ZERO_RESULTS":
        return False
    return data.get('results')[0]

def reverse_geocode(lat, lng, m_key):
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = "?latlng=%s,%s&key=%s" % (str(lat), str(lng), m_key)
    add_json = urllib.request.urlopen(base_url+params).read()
    data = literal_eval(add_json.decode('utf8'))
    if not data.get('results') or data.get('status') == "ZERO_RESULTS":
        return False
    return data.get('results')[0].get('formatted_address')

def address_to_coord(address, m_key):
    return tuple(geocode_address(address, m_key).get('geometry').get('location').values())

def formatted_address(address, m_key):
    return geocode_address(address, m_key).get('formatted_address')

def create_s3_client():
    return boto3.client('s3', aws_access_key_id=settings.AMAZON_S3_ACCESS_KEY_ID, aws_secret_access_key=settings.AMAZON_S3_SECRET_ACCESS_KEY)

def create_presigned_url(s3_client, filename, expiration=3600):
    """Generate a presigned URL to share an S3 object
    SOURCE: modification from  https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    # Generate a presigned URL for the S3 object
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': os.environ.get('AMAZON_S3_BUCKET_NAME'),
                                                            'Key': filename},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None
    # The response contains the presigned URL
    return response

def download_images(latitude, longitude, key, p, a=None, address = False):
    panoids = streetview.panoids(lat=latitude, lon=longitude)
    if not panoids:
        return False
    if not address:
        address = "NO_ADDRESS"
    obj_coord = (panoids[0]['lat'], panoids[0]['lon'])
    pic_coord = (latitude, longitude)
    angle = calculate_initial_compass_bearing(obj_coord, pic_coord)
    dates, urls = [], []

    if not settings.DOWNLOAD_LOCAL:
        s3 = create_s3_client()

    for elem in panoids:
        try:
            if isinstance(elem['year'], int):
                dates.append([ elem['year'], elem['month'] ])
                
                if settings.DOWNLOAD_LOCAL:
                    filename = streetview.api_download(elem['panoid'], angle, DOWNLOAD_DIR, key, address, a, p, year=elem['year'], month=elem['month'])
                else:
                    filename = streetview.upload_to_s3(elem['panoid'], angle, key, address, s3, a, p, settings.AMAZON_S3_BUCKET_NAME, year=elem['year'], month=elem['month'])

                # create url
                url = create_presigned_url(s3, filename)
                if not url:
                    # IF you see antioch from above, something went wrong
                    urls.append("https://upload.wikimedia.org/wikipedia/commons/a/af/San_Joaquin_Sacramento_confluence_at_Antioch_CA.jpg")
                else:
                    urls.append(url)
        except KeyError:
            pass
    # NO longer want to sort years or make into set BECAUSE we have months with which they are paired
    # years = list(set(years))
    # years.sort()
    return dates, urls

def sample_from_area(polygon_dict, n):
    point_list = [(p['lat'], p['lng']) for p in polygon_dict]
    poly = Polygon(point_list)
    min_x, min_y, max_x, max_y = poly.bounds
    sample = []
    while len(sample) < n:
        random_coord = [random.uniform(min_x, max_x), random.uniform(min_y, max_y)]
        random_point = Point(random_coord)
        if random_point.within(poly):
            sample.append({"lat":random_coord[0], "lng":random_coord[1]})
    return sample

def str_to_dic(string):
    # takes in the string returned from get_object_or_404
    # for the neighborhood definition and processes it into
    # a list of of dictionnaries.
    data = []
    divided = string.split('}')
    for point in divided[:-1]:
        coords = re.findall(r"[-+]?\d*\.\d+|\d+", point)
        data += [{"lat": float(coords[0]), "lng": float(coords[1])}]
    return data

def snap_point_to_address(lat, long, m_key):
    '''Given lat/lng, returns the {lat:, lng:} of the nearest address'''
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='
    params = "?latlng=%s,%s&key=%s" % (str(lat), str(long), m_key)
    my_json = urllib.request.urlopen(base_url+params).read()
    data = literal_eval(my_json.decode('utf8'))
    return data.get('results')[0]
