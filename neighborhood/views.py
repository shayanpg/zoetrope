from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import NeighborhoodCreationForm
from .models import Neighborhood
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, UpdateView, DeleteView

@login_required
def neighborhood(request):
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
        'title':'Neighborhoods',
        # 'neighborhood_list': Neighborhood.objects.all(),
        'neighborhood_list': Neighborhood.objects.filter(author=request.user.id),
        'form':form,
    }
    return render(request, 'neighborhood/index.html', context)

# TODO: Add Detail, Update, Delete Views
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
