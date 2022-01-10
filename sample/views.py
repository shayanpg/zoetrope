from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import streetview

from neighborhood.models import Neighborhood
import random
import re

from utils import str_to_dic, sample_from_area, download_images

@login_required
def sample(request, neighborhood_id):

    n = get_object_or_404(Neighborhood, pk=neighborhood_id)
    context = {
        'title':'Neighborhood Sampler',
        'neighborhood': n,
        'user': request.user,
        'sample': []
    }

    if request.method == "POST":
        num_points = int(request.POST.get('total_pic'))
        pts = str_to_dic(n.points)
        sample = sample_from_area(pts, num_points)
        context['sample'] = sample
        for p in sample:
            # FIXME: Temporary removal of downloading
            years = [2022]
            # years = download_images(p['lat'], p['lng'], request.user.gsv_api)
            if not years:
                messages.warning(request, f'No Photos Found for {str(p)}.')
            else:
                if len(years) > 1:
                    year_message = str(p) + " Years: " + ', '.join([str(year) for year in years[:-1]]) + ' and ' + str(years[-1])
                else:
                    year_message = str(p) + f" Year: {years[0]}"
                messages.info(request, year_message)
                messages.success(request, f'Photo(s) downloaded for {str(p)}.')
        # return render(request, 'sample/sample_success.html', context)
        return redirect('sample_success', neighborhood_id, str(sample))#, context=context)

    return render(request, 'sample/sample.html', context)

@login_required
def sample_success(request, neighborhood_id, sample):
    n = get_object_or_404(Neighborhood, pk=neighborhood_id)
    context = {
        'title':'Neighborhood Sampler',
        'neighborhood': n,
        'user': request.user,
        'sample': sample
    }
    return render(request, "sample/sample_success.html", context)
