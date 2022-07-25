from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from gsv import settings
from .forms import NeighborhoodCreationForm
from .models import Neighborhood
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, UpdateView, DeleteView

@login_required
def neighborhood(request):
    if request.method == 'POST':
        name = request.POST.get('nhoodname').strip()
        path = request.POST.get('newpath')
        redir_dest = 'draw'
        if len(name) == 0:
            messages.warning(request, "Error: Please try again with a valid name.")
        else:
            path = "[" + path + "]"
            path = path.replace("(", '{"lat":').replace(")", "}")
            # next line is bc the original format uses spaces only inside a tuple, never between
            path = path.replace(", ", ', "lng":')
            n = Neighborhood(author=request.user, name=name, points=path)
            n.save()
            redir_dest = n
            messages.success(request, f'Neighborhood {name} created.')
        print(name)
        print(path)
        # print(request.POST)
        return redirect(redir_dest)

    neighborhood_list = Neighborhood.objects.filter(author=request.user.id)
    context = {
        'title': 'Neighborhood Creator',
        'neighborhood_list': neighborhood_list,
        'MAPS_API_KEY': settings.MAPS_API_KEY
    }
    return render(request, 'neighborhood/nhood_index.html', context)

@login_required
def json_creator(request):
    if request.method == 'POST':
        form = NeighborhoodCreationForm(request.POST)
        if form.is_valid():
            n = form.save(commit=False)
            n.author = request.user
            form.save()
            messages.success(request, f'Neighborhood {n.name} created.')
        else:
            messages.error(request, "Form invalid. Please try again")
        return redirect('neighborhood')
    else:
        form = NeighborhoodCreationForm()

    context = {
        'title':'JSON Creator',
        'form':form,
    }
    return render(request, 'neighborhood/json_creator.html', context)

class NeighborhoodDetailView(DetailView):
    model = Neighborhood

class NeighborhoodUpdateView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Neighborhood

    fields = ['name', 'points']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user == self.get_object().author

class NeighborhoodDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = Neighborhood
    success_url = '/'

    def test_func(self):
        return self.request.user == self.get_object().author
