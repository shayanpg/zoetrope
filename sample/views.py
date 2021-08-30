from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import SampleForm

@login_required
def sample(request):
    # return render(request, 'sample/sample.html', {'title':'Neighborhood Sampler'})
    if request.method == 'POST':
        form = SampleForm(request.POST, user=request.user)
        if form.is_valid():
            # address = formatted_address(form.cleaned_data.get('address'), request.user.maps_api)
            # if not address:
            #     address = form.cleaned_data.get('address')
            # years = address_download(address, request.user.gsv_api, request.user.maps_api)
            # if not years:
            #     messages.warning(request, f'No Photos Found for {address}.')
            # else:
            #     if len(years) > 1:
            #         year_message = "Years: " + ', '.join([str(year) for year in years[:-1]]) + ' and ' + str(years[-1])
            #     else:
            #         year_message = f"Year: {years[0]}"
            #     messages.info(request, year_message)
            #     messages.success(request, f'Photo(s) downloaded for {address}.')
            return redirect('address')
    else:
        form = SampleForm(user=request.user)

    context = {
        'title':'Neighborhood Sampler',
        'form':form,
    }
    return render(request, 'sample/sample.html', context)
