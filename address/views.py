from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AddressForm
from utils import address_download, formatted_address

@login_required
def address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            #NOTE: If this breaks, check GCP Billing first
            address = formatted_address(form.cleaned_data.get('address'), request.user.maps_api)
            if not address:
                address = form.cleaned_data.get('address')
            years = address_download(address, request.user.gsv_api, request.user.maps_api)
            if not years:
                messages.warning(request, f'No Photos Found for {address}.')
            else:
                if len(years) > 1:
                    year_message = "Years: " + ', '.join([str(year) for year in years[:-1]]) + ' and ' + str(years[-1])
                else:
                    year_message = f"Year: {years[0]}"
                messages.info(request, year_message)
                messages.success(request, f'Photo(s) downloaded for {address}.')
            return redirect('address')
    else:
        form = AddressForm()

    context = {
        'title':'Address Finder',
        'form':form,
    }
    return render(request, 'address/address.html', context)
