from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from pull.models import Pull
from .forms import AddressForm
from .models import Address
from utils import download_images, geocode_address

@login_required
def address_form(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            #NOTE: If this breaks, check GCP Billing first
            geocoding = geocode_address(form.cleaned_data.get('address'), request.user.maps_api)
            # Default failure
            years, address = False, form.cleaned_data.get('address')
            if geocoding:
                address = geocoding.get('formatted_address')
                lat, lng = tuple(geocoding.get('geometry').get('location').values())
                # CREATE ADDRESS
                a = Address(name=address, lat=lat, lng=lng)
                a.save()
                fname = address.replace(' ', '_').replace(',', '')
                p = Pull(date=datetime.now().date(), author=request.user, address_id=a)
                p.save()
                years, files = download_images(lat, lng, request.user.gsv_api, p, a, fname)
            if not years: # Double checks that the download had results
                messages.warning(request, f'No Photos Found for {address}.')
            else:
                if len(years) > 1:
                    year_message = "Years: " + ', '.join([str(year) for year in years[:-1]]) + ' and ' + str(years[-1])
                else:
                    year_message = f"Year: {years[0]}"
                messages.info(request, year_message)
                messages.success(request, f'Photo(s) downloaded for {address}.')
            # CREATE ADDRESS w/ address
            return redirect('address')
    else:
        form = AddressForm()

    context = {
        'title':'Address Finder',
        'form':form,
    }
    return render(request, 'address/address.html', context)
