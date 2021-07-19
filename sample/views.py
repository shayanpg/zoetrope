from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def sample(request):
    return render(request, 'sample/sample.html', {'title':'Neighborhood Sampler'})
