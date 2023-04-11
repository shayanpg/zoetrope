from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.decorators import require_api_calls_remaining

from pull.models import Pull
from .forms import AddressForm
from .models import Address
from utils import download_images, geocode_address, MONTH_MAP
from gsv import settings

@login_required
@require_api_calls_remaining
def address_form(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            #NOTE: If this breaks, check GCP Billing first
            geocoding = geocode_address(form.cleaned_data.get('address'), settings.MAPS_API_KEY)
            # Default failure
            urls, address = [], form.cleaned_data.get('address')
            point = []
            if geocoding:
                address = geocoding.get('formatted_address')
                print("Address:", address)
                lat, lng = tuple(geocoding.get('geometry').get('location').values())
                point.append({"lat":lat, "lng":lng})
                # CREATE ADDRESS
                a = Address(name=address, lat=lat, lng=lng)
                a.save()
                fname = address.replace(' ', '_').replace(',', '')
                p = Pull(date=datetime.now().date(), author=request.user, address_id=a)
                p.save()
                dates, urls = download_images(lat, lng, settings.GSV_API_KEY, p, a, fname)

                # decrement API usage (including 1 for geocoding)
                request.user.dec_remaining_calls(1 + len(urls))
            if not urls: # Double checks that the download had results
                messages.warning(request, f'No Photos Found for {address}.')
            else:
                # if len(years) > 1:
                #     year_message = "Years: " + ', '.join([str(year) for year in years[:-1]]) + ' and ' + str(years[-1])
                # else:
                #     year_message = f"Year: {years[0]}"
                # messages.info(request, year_message)
                # messages.success(request, f'Photo(s) downloaded for {address}.')
                for i in range(len(urls)):
                    year, month = dates[i][0], dates[i][1]
                    message = address +" in " + MONTH_MAP[int(month)] + ", " + str(year)
                    messages.add_message(request, messages.INFO, message)
                    # print(message)
                    messages.add_message(request, messages.INFO, urls[i])
                    # print(urls[i])

            # CREATE ADDRESS w/ address
            return redirect('address_success', address, point)
    else:
        form = AddressForm()

    context = {
        'title':'Address Finder',
        'form':form,
    }
    return render(request, 'address/address.html', context)

@login_required
def address_success(request, address, point):
    image_data = messages.get_messages(request)

    for message in image_data:
        print("Sent_message:", message)

    context = {
        'address': address,
        'title':'Results',
        'no_info_messages': True
    }
    return render(request, "address/address_success.html", context)
