from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home/home.html', {'place':'holder'})

def about(request):
    return render(request, 'home/about.html', {'title':'About'})
