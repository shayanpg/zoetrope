from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}.')
            return redirect('gsv-home')
    else:
        form = UserCreationForm()
    context = {
        'title' : 'New User',
        'form' : form,
    }
    return render(request, 'users/register.html', context)
