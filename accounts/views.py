from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import ProfileCreationForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required

class RegisterView(CreateView):
    form_class = ProfileCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('update_profile')

    else:
        form = ProfileUpdateForm(instance=request.user)

    context = {
        'title':'Profile',
        'form':form,
    }
    return render(request, 'registration/update_profile.html', context)

@login_required
def calls_depleted(request):
    context = {
        'title':'Calls Depleted',
    }
    return render(request, 'calls_depleted.html',context)
