from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import NeighborhoodCreationForm
from .models import Neighborhood

@login_required
def neighborhood(request):
    if request.method == 'POST':
        form = NeighborhoodCreationForm(request.POST)
        if form.is_valid():
            n = form.save(commit=False)
            n.author = request.user
            form.save()
            messages.success(request, f'Neighborhood {n.name} created.')
            return redirect('neighborhood')
        else:
            messages.error(request, "Form invalid. Please try again")
    else:
        form = NeighborhoodCreationForm()

    context = {
        'title':'Neighborhoods',
        'neighborhood_list': Neighborhood.objects.all(),
        'form':form,
    }
    return render(request, 'neighborhood/index.html', context)
