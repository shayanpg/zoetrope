# from django.shortcuts import render

# Create your views here.
# from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib import messages
#
# def register(request):
#     # if request.method == 'POST':
#     #     form = UserCreationForm(request.POST)
#     #     if form.is_valid():
#     #         form.save()
#     #         username = form.cleaned_data.get('username')
#     #         messages.success(request, f'Account created for {username}.')
#     #         return redirect('gsv-home')
#     # else:
#     #     form = UserCreationForm()
#     context = {
#         'title' : 'New User',
#         # 'form' : form,
#     }
#     return render(request, 'accounts/register.html', context)

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import ProfileCreationForm

class RegisterView(CreateView):
    form_class = ProfileCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'
