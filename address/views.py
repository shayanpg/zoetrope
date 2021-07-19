from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AddressForm

import streetview
import urllib
from ast import literal_eval
import json
import csv
import re
import math
import random

from math import sin, cos, sqrt, atan2, radians

@login_required
def address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data.get('address')
            messages.success(request, f'Photos downloaded for {address}.')
            return redirect('address')
    else:
        form = AddressForm()

    context = {
        'title':'Address Finder',
        'form':form,
    }
    return render(request, 'address/address.html', context)


@login_required
def response(request):
    address = request.POST['address']
    sv_key = request.user.gsv_api
    m_key = request.user.maps_api
    years = address_download(address, sv_key, m_key)
    context = {'title':'Download Images',
        'sv_key' : sv_key,
        'm_key' : m_key,
        'address' : address,
        'years' : ', '.join([str(year) for year in years[:-1]]) + ' and ' + str(years[-1]),
    }
    return render(request, 'address/response.html', context)

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

def address_to_coord(address, m_key):
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?address='
    add_url = base_url + address.replace(' ', '+') + '&key=' + m_key
    add_json = urllib.request.urlopen(add_url).read()
    data = literal_eval(add_json.decode('utf8'))
    return tuple(data.get('results')[0].get('geometry').get('location').values())

def download_images(latitude, longitude, key, address = False):
    panoids = streetview.panoids(lat=latitude, lon=longitude)
    obj_coord = (panoids[0]['lat'], panoids[0]['lon'])
    pic_coord = (latitude, longitude)
    angle = calculate_initial_compass_bearing(obj_coord, pic_coord)
    print('ANGLE:', angle)
    years = []
    for elem in panoids:
        try:
            if type(elem['year']) == int:
                years.append(elem['year'])
                if address != False:
                    streetview.api_download_address(elem['panoid'], angle, './downloads/', key, address, year = elem['year'])
                    print('Picture for', elem['month'], elem['year'], 'downloaded')
                else:
                    streetview.api_download(elem['panoid'], angle, './downloads/', key)
        except KeyError:
            pass
    years = list(set(years))
    years.sort()
    return years

def address_download(address, sv_key, m_key):
    print('Downloading pictures for address:', address)
    # extracts the latitude and longitude from the address using the maps api
    coords = address_to_coord(address, m_key)
    lat, lon = coords[0], coords[1]
    # name the file
    fname = address.replace(' ', '_').replace(',', '')
    # download the street view images for the address using the extracted lat, long
    return download_images(lat, lon, sv_key, fname)
