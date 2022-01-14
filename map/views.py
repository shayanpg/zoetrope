from django.shortcuts import render, redirect, get_object_or_404
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


from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
# 
# @login_required
# def map(request):
#     context = {'title':'map', 'user': request.user}
#     return render(request, 'map/map.html', context)

@login_required
def polygon(request, neighborhood_id):

    n = get_object_or_404(Neighborhood, pk=neighborhood_id)

    context = {
        'neighborhood': n,
        'user': request.user
    }

    return render(request, 'map/polygon.html', context)
