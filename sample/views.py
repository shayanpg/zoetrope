from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from neighborhood.models import Neighborhood
from address.models import Address

from datetime import  datetime

from pull.models import Pull
from utils import str_to_dic, sample_from_area, download_images, reverse_geocode

@login_required
def index(request):
    neighborhood_list = Neighborhood.objects.filter(author=request.user.id)
    context = {
        'neighborhood_list': neighborhood_list,
        'user': request.user
    }

    return render(request, 'sample/sampling_index.html', context)

@login_required
def sample_points(request, neighborhood_id):

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
        pull = Pull(date=datetime.now().date(), author=request.user, neighborhood_id=n)
        pull.save()
        for p in sample:
            # CREATE ADDRESS w/ reverse_geocode
            address = reverse_geocode(p['lat'], p['lng'], request.user.maps_api)
            if not address:
                address = '"No Address for (%s, %s)"' % (p['lat'], p['lng'])
            else: # Only need to save addresses that actually exist -- also good measure against DOS attacks
                a = Address(name=address, lat=str(p['lat']), lng=str(p['lng']))
                a.save()
                a.neighborhoods.add(n)
            # years = [2022] # FOR DEBUGGING (speed up page loading when download not required)
            print("Address:", address)
            fname = address.replace(' ', '_').replace(',', '')
            dates, urls = download_images(p['lat'], p['lng'], request.user.gsv_api, pull, a, fname)
            assert len(dates) == len(urls)
            if not urls:
                messages.warning(request, f'No Photos Found for "{address}".')

            month_map = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June", 7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}
            # message_to_url = dict()
            for i in range(len(urls)):
                year, month = dates[i][0], dates[i][1]
                message = address +" in " + month_map[int(month)] + ", " + str(year)
                # message_to_url[message] = urls[i]
                messages.add_message(request, messages.INFO, message)
                # print(message)
                messages.add_message(request, messages.INFO, urls[i])
                # print(urls[i])

        return redirect('sample_success', neighborhood_id, str(sample).replace("'", '"'))

    return render(request, 'sample/sample.html', context)

@login_required
def sample_success(request, neighborhood_id, sample):
    n = get_object_or_404(Neighborhood, pk=neighborhood_id)
    image_data = messages.get_messages(request)

    for message in image_data:
        print("Sent_message:", message)

    context = {
        'title':'Neighborhood Sample Success Page',
        'neighborhood': n,
        'user': request.user,
        'sample': sample,
        # 'message_to_url': message_to_url
        'no_info_messages': True
    }
    return render(request, "sample/sample_success.html", context)
