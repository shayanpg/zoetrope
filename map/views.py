# from django.shortcuts import render, redirect, reverse
# from django.conf import settings
#
# def map(request):
#
# 	lat_a = request.GET.get("lat_a", None)
# 	long_a = request.GET.get("long_a", None)
# 	# lat_b = request.GET.get("lat_b", None)
# 	# long_b = request.GET.get("long_b", None)
# 	# lat_c = request.GET.get("lat_c", None)
# 	# long_c = request.GET.get("long_c", None)
# 	# lat_d = request.GET.get("lat_d", None)
# 	# long_d = request.GET.get("long_d", None)
#
#
# 	#only call API if all 4 addresses are added
# 	# if lat_a and lat_b and lat_c and lat_d:
# 	# 	directions = Directions(
# 	# 		lat_a= lat_a,
# 	# 		long_a=long_a,
# 	# 		lat_b = lat_b,
# 	# 		long_b=long_b,
# 	# 		lat_c= lat_c,
# 	# 		long_c=long_c,
# 	# 		lat_d = lat_d,
# 	# 		long_d=long_d
# 	# 		)
# 	# else:
# 	# 	return redirect(reverse('home'))
#
# 	context = {
# 	"google_api_key": settings.GOOGLE_MAPS_API_KEY,
# 	# "base_country": settings.BASE_COUNTRY,
# 	"lat_a": lat_a,
# 	"long_a": long_a,
# 	# "lat_b": lat_b,
# 	# "long_b": long_b,
# 	# "lat_c": lat_c,
# 	# "long_c": long_c,
# 	# "lat_d": lat_d,
# 	# "long_d": long_d,
# 	"origin": f'{lat_a}, {long_a}',
# 	# "destination": f'{lat_b}, {long_b}',
# 	# "directions": directions,
#
# 	}
# 	return render(request, 'map/map.html', context)

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.views import generic
import pdb

import streetview
from datetime import date
from calendar import monthrange
import math
import urllib
from ast import literal_eval
import pathlib

from neighborhood.models import Neighborhood
from shapely.geometry import Polygon, Point
import random
import re
# Create your views here.

class Save_Request:
    def __init__(self, request):
        html_data = request.POST
        self.critical_date = {'year': int(html_data['c_year']), 'month': int(html_data['c_month']), 'day': int(html_data['c_day'])}
        self.num_points = int(html_data["point_freq"])
        print('Sample size', int(html_data["total_pic"]))
        self.sample_size = int(html_data["total_pic"])

def map(request):
    context = {'title':'map'}
    return render(request, 'map/map.html', context)

def index(request):
    neighborhood_list = Neighborhood.objects.all()
    context = {
        'neighborhood_list': neighborhood_list,
        'user': request.user
    }

    return render(request, 'map/index.html', context)


def polygon(request, neighborhood_id):

    n = get_object_or_404(Neighborhood, pk=neighborhood_id)

    context = {
        'neighborhood': n,
        'user': request.user
    }

    return render(request, 'map/polygon.html', context)

    # template = loader.get_template('map/polygon.html')
    # return HttpResponse(template.render({}, request))
def sample_from_area(polygon_dict):
    point_list = [(p['lat'], p['lng']) for p in polygon_dict]
    poly = Polygon(point_list)
    min_x, min_y, max_x, max_y = poly.bounds
    sample = []
    while len(sample) == 0:
        random_coord = [random.uniform(min_x, max_x), random.uniform(min_y, max_y)]
        random_point = Point(random_coord)
        if random_point.within(poly):
            sample.append(random_coord)
    return random_coord


def str_to_dic(string):
    # takes in the string returned from get_object_or_404
    # for the neighborhood definition and processes it into
    # a list of of dictionnaries.
    data = []
    divided = string.split(')')
    for point in divided[:-1]:
        coords = re.findall(r"[-+]?\d*\.\d+|\d+", point)
        data += [{"lat": float(coords[0]), "lng": float(coords[1])}]
    return data


# def download_some_images(request, neighborhood_id):
#
#     # Gets all the specified values in the html form
#     download_information = Save_Request(request)
#     # print('Num Points', download_information.num_points)
#
#     # Retrieves and reformats the neighborhood's coordinates
#     n = get_object_or_404(Neighborhood, pk=neighborhood_id)
#     polygon_dict = str_to_dic(n.polygon_string)
#
#     # Sampling Checking Downloading loop
#     num_dwl = 0
#     while num_dwl < 3: #download_information.num_points:
#         # sample a point within the relevant area
#         s_point = sample_from_area(list(polygon_dict))
#         lat = s_point[0]
#         lng = s_point[1]
#         # get the api keys
#         sv_key = request.user.gsv_api
#         m_key = request.user.maps_api
#         # approximate the lat lng based on available address
#         nearest_address = snap_point_to_address(lat, lng, m_key)
#         lat = nearest_address['geometry']['location']['lat']
#         lng = nearest_address['geometry']['location']['lng']
#         formatted_address = nearest_address['formatted_address']
#         # Get the panoids for that particular point
#         panoids = streetview.panoids(lat=lat, lon=lng)
#         # filter the panoids
#         # filt_p = specific_year_filt(panoids, download_information.critical_date['year'])
#         # filt_p = filter_panoids('Filter', panoids)
#         if len(panoids) != 0:
#             num_dwl += 1
#             # panoid_dwl(download_information, lat, lng, filt_p, sv_key, formatted_address)
#             download_images(download_information, lat, lng, sv_key, formatted_address)
#
#     template = loader.get_template('map/index.html')
#     return HttpResponse(template.render({}, request))

def snap_point_to_address(lat, long, m_key):
    '''Given lat/lng, returns the {lat:, lng:} of the nearest address'''
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='
    coord_url = base_url + str(lat) + ',' + str(long) + '&key=' + m_key
    my_json = urllib.request.urlopen(coord_url).read()
    data = literal_eval(my_json.decode('utf8'))
    return data.get('results')[0]


def filter_panoids(panoids, require_year=True, before_after_date=None):
    '''
    The idea here is to add more optional parameters which will allow us to filter panoids in different ways.
    If require_year=True, then the panoids list will be filtered to include only panoids
    with an attached year.
    If before_after_date is given, then the panoid list will be filtered to include only
    the panoids which most closely sandwich the before_after_date
    Paramters:
        - panoids: A list of panoid dictionaries, as returned by streetview.panoids()
        - requrie_year: boolean.  If true, all panoids without a 'year' will be filtered out
        - A datetime.date object.  If present, the panoid dictionary will be filtered to
             include only the panoids which most closely sandwich before_after_date
    '''
    filtered_panoids = []

    if require_year:
        for p in panoids:
            if 'year' in p:
                filtered_panoids.append(p)

    if before_after_date:

        closest_pre_date = None
        closest_post_date = None
        p_before = None
        p_after = None

        for p in filtered_panoids:
            year = month = day = None
            try:
                year = p['year']
                # We want to be as conservative as possible when guessing when a panorama was taken.
                if 'month' in p:
                    month = p['month']
                    if month < before_after_date.month:
                        day = monthrange(year, month)[1]
                    elif month > before_after_date.month:
                        day = 1
                    else:
                        # this panoid was taken during the same month and year as our before_after_date.
                        # we can't tell for sure whether it was taken before or after, so we've got to ignore it
                        continue
                # if no month is specified, we assume 12/31 or 1/1
                elif year < before_after_date.year:
                    month = 12
                    day = 31
                elif year > before_after_date.year:
                    month = day = 1
                else:
                    # If no month is specified and our panorama is taken in the same year as our before_after_date...
                    # we can't tell for sure whether it came before or after.
                    continue

                pano_date = date(year, month, day)
                if pano_date < before_after_date:
                    if (not p_before) or (pano_date > closest_pre_date):
                        p_before = p
                        closest_pre_date = pano_date
                elif pano_date > before_after_date:
                    if (not p_after) or (pano_date < closest_post_date):
                        p_after = p
                        closest_post_date = pano_date

            except KeyError:
                # if there is no year, we'll ignore the panoid
                pass

            filtered_panoids = [p_before, p_after]

    return filtered_panoids

def download_images(dwl_inf, latitude, longitude, sv_key, address, angle='AIM', before_after_date=None):
    '''Downloads all pictures (with recorded years) taken nearest the given lat/long and oriented tat given angle. Save them to /tmp/gsv/photos
        Paramters:
            - lattitude: string, lattitude of point we want an image of
            - longitude: string, longitude of piont we want an image of
            - sv_key: Google Streetview API key https://developers.google.com/maps/documentation/streetview/
            - angle: can be any number of degrees (integer), or 'AIM'.  If 'AIM', we will try to orient the image toward the given lat/long
            - before_after_date: a datetime.date object.  If present, only the two images which most closely surround the given date will be downloaded
    '''
    panoids = streetview.panoids(lat=latitude, lon=longitude)

    # filtered_panoids = filter_panoids(panoids, True, dwl_inf.critical_date)
    filtered_panoids = panoids

    num_points = dwl_inf.num_points
    angle_increment = int(round(360 / num_points))

    for elem in filtered_panoids:
        print(elem['year'])
        try:
            if type(elem['year']) == int:
                if angle == 'AIM':
                    # we need to aim each panoid at the given lat/long
                    orientation = orient_pic(elem, (latitude, longitude))
                    print('orientation: {}'.format(orientation))
                else:
                    orientation = angle

                print('orientation', type(orientation))
                print('angle_increment', type(angle_increment))
                print('num_points', type(num_points))

                for orientation_i in range(int(round(orientation)), int(round(orientation)) + angle_increment * (num_points - 1), angle_increment):
                    filepath = '/tmp/gsv/photos/{}/'.format(address)

                    print('Picture for', elem['month'], elem['year'], 'downloaded', angle)
                    print('Address: '+address)
                    pathlib.Path(filepath).mkdir(parents=True, exist_ok=True)
                    streetview.api_download(elem['panoid'], orientation_i, filepath, sv_key,
                                            fname='{}_{}_{}_{}'.format(elem['year'], elem['month'], elem['panoid'], str(orientation_i)))
        except KeyError:
            print("aw shucks, this should have been filtered out")
            # There was no year attached to the panoid
            pass

def calculate_initial_compass_bearing(pointA, pointB):
    """
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
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

def orient_pic(pano_dict, obj_pos):
    """
    Calculates the orientation necessary (in bearings) to take a picture
    of a desired object at position obj_pos
    :Parameters:
        - pano_dict: dict returned by the streetview.panoids method
        - obj_pos: tuple of (lat, long)
    :Returns:
        - bearing in degrees (float)
    """
    pano_tuple = (pano_dict["lat"], pano_dict["lon"])
    return calculate_initial_compass_bearing(pano_tuple, obj_pos)
