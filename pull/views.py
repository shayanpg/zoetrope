from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.decorators import require_api_calls_remaining

from neighborhood.models import Neighborhood
from address.models import Address
from pull.models import Pull

@login_required
def history(request):
    pull_list = Pull.objects.filter(author=request.user.id).order_by('-date')
    context = {
        'pull_list': pull_list,
    }

    return render(request, 'pull/history.html', context)
