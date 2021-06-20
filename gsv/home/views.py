from django.shortcuts import render

# Create your views here.

posts = [
    {
        'author': 'SPG',
        'title': 'P1',
        'content': 'First',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'JD',
        'title': 'P2',
        'content': 'SECOND',
        'date_posted': 'August 29, 2018'
    }
]

def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'home/home.html', context)

def about(request):
    return render(request, 'home/about.html', {'title':'About'})
